import subprocess
from multiprocessing import Process, Queue
import os
import re
from turtle import reset
from unittest import result
import time
from threading import Thread
import signal
import sys

import utils


class MCC_Process(Process):
    def __init__(self, path_dic, in_queue, out_queue, put_command_queue, get_command_queue, state_queue, data, allow_restart):
        Process.__init__(self)
        self.daemon = True  #设置为守护进程（随主进程关闭）
        self.dir_path = path_dic["dir_path"]    #各个文件路径
        self.exe_path = path_dic["exe_path"]
        self.ini_path = path_dic["ini_path"]
        self.log_path = path_dic["log_path"]
        self.in_queue = in_queue    #通信队列，实现命令输入
        self.out_queue = out_queue  #通信队列，用于接收子进程输出
        self.get_command_queue = put_command_queue  #通信队列，用于接收子进程的自定义指令
        self.put_command_queue = get_command_queue  #通信队列，用于向主进程发送自定义指令
        self.state_queue = state_queue  #通信队列，用于传递假人状态
        self.result = None
        self.data = data
        self.name = data[5]
        self.ppid = os.getppid()
        self.allow_restart = allow_restart
        self.connect = False
        self.force_close = False

        self.state_dic =   {
            "alive" : None,
            "health" : None,
            "saturation" : None,
            "level" : None,
            "total_experience" : None
            }

        print(f"[DEBUG]待执行的子进程{self.name}已创建，父进程为（{self.ppid}）")

    def run(self):
        print(f"[DEBUG]交互子进程{self.name}（{self.pid}）开始执行，父进程为（{self.ppid}）")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE    #隐藏发布版本MCC的命令行窗口

        self.result = subprocess.Popen(
            [self.exe_path],          # 命令及参数（列表或字符串）
            bufsize=-1,          # 缓冲区大小（默认-1表示系统默认）
            stdin=subprocess.PIPE,          # 标准输入
            stdout=subprocess.PIPE,         # 标准输出
            stderr=subprocess.PIPE,         # 标准错误
            close_fds=True,      # 关闭子进程继承的文件描述符
            shell=False,         # 是否通过shell执行
            cwd=self.dir_path,   # 子进程工作目录
            env=None,            # 环境变量（字典）
            startupinfo=startupinfo,    # Windows控制窗口样式（如隐藏）
            creationflags=0,     # Windows创建标志（如CREATE_NO_WINDOW）
            text=True,           # 文本模式（Python 3.7+，等同于universal_newlines）
            encoding="utf-8",       # 文本编码（如'utf-8'）
            errors=None          # 编码错误处理
            )
        
        print(f"[DEBUG]交互子进程（{self.pid}）对应MCC子进程（{self.result.pid}）")

        self.listening_thread = Thread(name=f"{self.name}-listening_thread", target=self.listening)   #创建线程监听MCC输出
        self.listening_thread.start()
        self.state_thread = Thread(name=f"{self.name}-state_thread", target=self.get_state)   #创建线程实时获取假人信息
        self.state_thread.start()
        self.get_command_thread = Thread(name=f"{self.name}-get_command_thread", target=self.get_command)    #创建线程接收主进程命令
        self.get_command_thread.start()

        while self.result.poll() == None and not self.force_close:   #进程执行时循环
            if not self.in_queue.empty():   #接受队列的命令
                send_text = self.in_queue.get(False)
                print(f"[DEBUG]子进程{self.name}（{self.pid}）接收到命令\"{send_text}\"")
                self.result.stdin.write(send_text+"\n")
                self.result.stdin.flush()

        if self.allow_restart:
            self.put_command_queue.put("restart", False)
        elif self.force_close:
            pass
        else:
            self.put_command_queue.put("close", False) 
        
        self.listening_thread.join()
        self.state_thread.join()
        print(f"[DEBUG]子进程{self.name}（{self.pid}）已终止，父进程为（{self.ppid}）,退出状态码{self.result.poll()}")
        self.window_print("[MCCGUI] 进程已成功关闭!")

    def listening(self):
        '''监听子进程输出'''
        print(f"[DEBUG]子线程{self.listening_thread.name}（{self.listening_thread.ident}）已就绪，开始监听MCC进程的输出")

        while self.result.poll() == None:
            for text in self.result.stdout: #获取MCC输出
                allow_output = True
                ansi_text = text.strip()    
                out_text = re.sub(r'\x1b\[[0-9;]*m', '', ansi_text)
                health_match = re.match(r"^\[MCC\] Health: (\d+\.?\d*), Saturation: (\d+\.?\d+), Level: (\d+\.?\d*), TotalExperience: (\d+\.?\d*)", out_text)
                if health_match:
                    allow_output = False

                if allow_output:
                    print(f"子进程{self.name}（{self.pid}<-{self.result.pid}）>>" , end="")    

                if re.match(r"^\[ERROR\]", out_text):    #匹配输出内容
                    print(f"MCC报错>{re.sub(r"\[ERROR\]", "", ansi_text)}")
                    print(f"[DEBUG]{self.name}子进程（{self.pid}）发生报错！")

                elif re.match(r"^\[MCC\]", out_text):
                        

                    if out_text == "[MCC] Connection has been lost.":
                        self.window_print(f"[MCCGUI] 检测到断开连接，即将重连。。。")
                        self.connect = False
                        self.put_command_queue.put("restart", False)

                    elif re.match(r"^\[MCC\] You are dead.", out_text):
                        self.window_print(f"[MCCGUI] 检测到角色死亡，请重生。。。")
                        self.put_command_queue.put("died", False)

                    else:
                        if health_match:
                            #print("匹配成功！ " ,  health_match.groups())
                            health, saturation, level, total_experience = map(float, health_match.groups())
                            self.state_dic.update({
                                "alive" : health > 0,
                                "health" : round(health, 1),
                                "saturation" : round(saturation, 1),
                                "level" : int(level),
                                "total_experience" : int(total_experience),
                                })
                            self.state_queue.put(self.state_dic, False)
                            #self.window_print(f"[MCCGUI] 当前状态：{self.state_dic}")

                    if allow_output:
                        print(f"MCC消息>{re.sub(r"\[MCC\]", "", ansi_text)}")

                elif re.match("^▌", out_text):
                    if allow_output:
                        print(f"服务器消息>{ansi_text}")

                else:
                    if out_text == r"Type '/quit' to leave the server.":
                        self.window_print("[MCCGUI] 连接成功，后续允许重连")
                        self.allow_restart = True
                        self.connect = True
                        self.put_command_queue.put("connect", False)

                    if allow_output:
                        print(ansi_text)

                if allow_output:
                    self.out_queue.put(ansi_text, False)
    
    def get_state(self):
        print(f"[DEBUG]子线程{self.state_thread.name}（{self.state_thread.ident}）已就绪，获取假人{self.name}状态")

        while self.result.poll() == None:
            if self.connect:
                self.result.stdin.write("/health" + "\n")
                self.result.stdin.flush()
            time.sleep(1)
    
    def get_command(self):
        '''接收主进程的命令'''
        print(f"[DEBUG]子线程{self.get_command_thread.name}（{self.get_command_thread.ident}）已就绪，开始接收主进程（{self.ppid}）的命令")
        
        while True:
            if not self.get_command_queue.empty():
                command = self.get_command_queue.get(False)
                if command == "close_mcc":
                    print(f"[DEBUG]子进程（{self.pid}）接收到来自主进程的信号“close_mcc”,即将强制关闭MCC进程")
                    self.close_MCC()

    def close_MCC(self):
        '''强制关闭子进程和MCC'''
        print("?")
        if self.result != None:
            print(f"[DEBUG]交互子进程（{self.pid}）和MCC子进程（{self.result.pid}）已终止")
            self.result.terminate()
            self.result.wait()
        else:
            print(f"[DEBUG]交互子进程（{self.pid}）已终止")
        self.force_close = True

    def window_print(self, text):
        '''输出内容到队列和输出流(输出到队列的内容会自动进入日志)'''
        print(text)
        self.out_queue.put(text, False)
