'''
Minecraft命令行工具来自MCC开发者团队，Mirence对其源码进行了部分修改以适配该MCCGUI程序

v0.1    实现账户的添加、删除和账户启动
v0.2    实现账户信息的编辑功能
v0.3    1.改用多进程启动MCC，实现正常向MCC输入文本；
        3.实现向服务器发送命令或消息；
        4.统一文字编码，将所有文字改为中文。
v0.3.1  1.仅在MCC进程启动时可以发送消息，仅未启动时可以编辑和删除账户；
        2.MCC子进程异常关闭（非手动退出）时会自动同步关闭状态和按键；
v0.4    1.采用多线程实现监听MCC输出;
        2.发送功能升级为输入输出窗口,可以发送消息的同时还可以查看MCC的输出内容（包括服务器内消息）；
v0.4.1  1.监听窗口始终可以打开，且窗口打开时可以操作主窗口;
        2.每个账户只能打开一个监听窗口，当打开已打开的监听窗口时，会将监听窗口重新显示在屏幕顶层并聚焦；
        3.可以同时打开多个账户的监听窗口。
        4.过滤原MCC输出中的ANSI转移符。
v0.4.2  1.修复了反复打开各个窗口的内存泄漏问题；
        2.监听内容会输出到日志并保存；
        3.在控制窗口加入控制栏，包含启动/退出键，未来可加入更多功能；
        4.监听窗口升级为控制窗口，关闭窗口后能够继续监听MCC的输出，重新打开后会读取日志恢复先前内容，同时显示关闭窗口期间监听的内容；
        5.MCC未启动时、发送消息为空时无法发送。
v0.4.3  1.控制窗口内的启动按键可正常使用；
        2.能够分辨MCC的报错输出、普通输出和服务器消息输出；
        3.MCC报错后会立刻关闭该进程；
v0.5    1.新增掉线自动重连功能：重新连接服务器若干次，仍然连接不成功后将会关闭进程，仅账户在线期间掉线可以触发重连，启动时的连接失败不会触发重连；
        2.控制界面新增“重连”按钮：点击后会直接重启MCC；
        3.优化监听窗口的内容显示：当滚动条处于最低处时会向下自动显示新的消息内容，否则保持不动。
        4.内存优化：MCC重新启动时若上一个相同进程未关闭，则会强制关闭。
v0.5.1  1.在控制窗口界面按下回车键可以发送内容；
        2.发送消息后监听窗口滚动条将移到最低处;
        3.打开监听窗口会会自动聚焦到消息发送文本框。
v0.6    1.新增重生功能：死亡状态下“重生”按钮亮起，点击“重生”按钮可以重生；
        2.新增假人状态显示窗口：可以显示假人当前的存活状态、生命值、饥饿值、经验值与经验等级；
        3.报错退出优化：采用了MCC自带的报错关闭进程的机制；
        4.重连按钮优化：仅进程开启时可以进行重连。
v0.6.1  1.新增发送消息缓存功能：发送过的消息或命令会被缓存（关闭程序后会清空），按下按键“↑”或“↓”可以快速输入之前输入过的内容。
        2.打开已关闭的控制窗口时会将监听窗口的滚动条移动至最下方；
        3.修复了重连和退出游戏后假人状态不变的问题，现在假人不在线时状态显示均为未知；
v0.6.2  1.修复了发布版本在window系统下的MCC子进程无法被正确创建的问题；
        2.隐藏了发布版本的MCC自身弹出的命令行窗口；
        3.设计了MCCGUI的初代图标。
v0.6.3  1.修复了多种情况下交互子进程和MCC子进程未能正确关闭的问题（包括但不限于强制关闭MCC、重连、关闭主程序）；
        2.监听窗口和日志内添加了更多的调试信息（[MCCGUI]开头的消息)。
         
'''

from genericpath import isfile
import glob
from nt import terminal_size
from re import M, sub
from statistics import variance
from struct import pack
from tkinter import *
import tkinter
import tkinter.scrolledtext
from turtle import title
from wsgiref import validate
from accounts import *
from numpy import insert, log
import os
from multiprocessing import Queue, freeze_support
import shutil
import setini
import start
import logging
import sys

accounts=Accounts()
MangoCraft = True
version = "0.6.3"



class MCC_GUI():
    '''主窗口类'''
    def __init__(self):
        global SCREEN_WIDTH,SCREEN_HEIGHT #窗口
        self.window=Tk()
        self.window.title("MCC GUI 可交互式工具")
        self.window.iconbitmap("bin/AppIcon.ico")
        self.window.protocol("WM_DELETE_WINDOW", self.close)    #关闭窗口后强制关闭主进程
        self.width=800
        self.height=600
        SCREEN_WIDTH=self.window.winfo_screenwidth()
        SCREEN_HEIGHT=self.window.winfo_screenheight()
        self.window.geometry(f"{self.width}x{self.height}+{(SCREEN_WIDTH-self.width)//2}+{(SCREEN_HEIGHT-self.height)//3}")     #居中显示
        self.window.resizable(False,False)
        self.canvas=Canvas(self.window,width=self.width, height=self.height)
        self.main_frame=Frame(self.canvas,width=self.width)
        self.canvas.create_window((0,0),window=self.main_frame,anchor="nw",width=self.width) #创建可以滚动的框架
        self.main_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.pack()

        self.scro=Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)   #滚动条
        self.scro.pack(side="right",fill="y")
        self.canvas.configure(yscrollcommand=self.scro.set)

        self.accounts_init = False

        self.button()
        self.show_accounts()

    def button(self):
        '''主窗口按钮初始化'''
        self.add_account_button=Button(self.main_frame,text="添加账户",command=self.open_add_account_window)
        self.add_account_button.pack(ipadx=5, ipady=2, pady=5)

    def open_add_account_window(self):
        '''打开添加账户窗口'''
        self.add_account_window=AddAccount(self)

    def show_accounts(self):
        '''读取并展示已保存的账户,同时校验保存的数据'''
        if self.accounts_init:
            for i in self.accounts:
                i.frame.destroy()
        self.accounts_init = True
        self.accounts=[]
        self.count=accounts.len()
        print("[DEBUG]账号数量",self.count)
        for i in range(self.count):
            self.verification(accounts.read(i),i)
            self.accounts.append(AccountFrame(self,i,accounts.read(i)))
            self.accounts[i].frame.pack(fill="both", padx=4)
            print(f"[DEBUG]账户{i}已生成")

    def update_account(self):
        '''更新账户列表'''
        self.show_accounts()

    def verification(self,user_data,i):
        '''校验并修复文件'''
        num=str(i+1000)[1:]
        flag=False
        if os.path.isdir(f"config/app_data/{num}"):
            if os.path.isfile(f"config/app_data/{num}/MinecraftClient.exe"):
                flag=True
        if not flag:
            creat_user_file(num,user_data)
    
    def close(self):
        print(f"用户关闭主窗口，主进程以及所有子进程都将将强制关闭！")
        self.window.destroy()
        for account in self.accounts:
            if account.exe != None:
                account.close_MCC()
        sys.exit(0)

class AddAccount:
    '''添加账户窗口类'''
    def __init__(self,master):
        self.window=Toplevel(master.window)
        self.window.title("添加账户")
        self.width=300
        self.height=230
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False,False)
        self.window.grab_set()      #禁用父窗口
        self.window.geometry(f"{self.width}x{self.height}+{master.window.winfo_x()+(master.window.winfo_width()-self.width)//2}+{master.window.winfo_y()+(master.window.winfo_height()-self.height)//2}")  #窗口居中显示
        self.way_single_ver=StringVar() #登录方式选项初始化
        self.way_single_ver.set("Microsoft")
        if MangoCraft: self.way_single_ver.set("Yggdrasil") #芒果方块定制
        
        self.frame()
        self.spawn()

    def spawn(self):
        '''生成组件(不包括框架)'''
        self.ent()
        self.button()
        self.text()

    def text(self):
        '''文本消息'''
        self.warning=Label(self.frame3,fg="red")
        self.warning.pack()

    def frame(self):
        '''框架'''
        self.frame1=Frame(self.window) #装登录方式
        self.frame1.pack(pady=10)
        self.frame2=Frame(self.window) #装账密
        self.frame2.pack(pady=0)
        self.frame3=Frame(self.window) #装登录按钮
        self.frame3.pack(pady=10)

    def ent(self):
        '''选择器、文本框'''
        self.row=0

        self.way_label=Label(self.frame1,text="登录方式:")  #登录方式
        self.way_label.grid(row=self.row,column=0)
        self.way1_single=Radiobutton(self.frame1,text="正版账户",variable=self.way_single_ver,value="Microsoft",command=self.update)
        self.way1_single.grid(row=self.row,column=1)
        self.way2_single=Radiobutton(self.frame1,text="第三方认证账户",variable=self.way_single_ver,value="Yggdrasil",command=self.update)
        self.way2_single.grid(row=self.row,column=2)
        self.row+=1

        self.account_label=Label(self.frame2,text="账号:") #账号
        self.account_label.grid(row=self.row,column=0)
        self.account_ent=Entry(self.frame2)
        self.account_ent.grid(row=self.row,column=1)
        self.row+=1

        self.password_label=Label(self.frame2,text="密码:") #密码
        self.password_label.grid(row=self.row,column=0)
        self.password_ent=Entry(self.frame2,show="*")
        self.password_ent.grid(row=self.row,column=1)
        self.row+=1

        self.server_label=Label(self.frame2,text="游戏服务器IP:") #服务器IP
        self.server_label.grid(row=self.row,column=0)
        self.server_ent=Entry(self.frame2)
        self.server_ent.grid(row=self.row,column=1)
        if MangoCraft: self.server_ent.insert(0, "bot.server.mangocraft.cn") #芒果方块定制
        self.row+=1

        if self.way_single_ver.get()=="Yggdrasil": 
            self.login_server_label=Label(self.frame2,text="认证服务器IP")  #认证服务器
            self.login_server_label.grid(row=self.row,column=0)
            self.login_server_ent=Entry(self.frame2)
            self.login_server_ent.grid(row=self.row,column=1)   
            if MangoCraft: self.login_server_ent.insert(0, "skin.prinzeugen.net")   #芒果方块定制
            self.row+=1

            self.role_label = Label(self.frame2, text = "角色名")    #登录角色
            self.role_label.grid(row=self.row,column=0)
            self.role_ent=Entry(self.frame2)
            self.role_ent.grid(row=self.row,column=1)
            self.row+=1

    def button(self):
        '''按钮'''
        self.login_button=Button(self.frame3,text="创建",command=self.login) #登录按钮
        self.login_button.pack()

    def update(self):
        '''刷新组件'''
        for i in (self.frame1,self.frame2,self.frame3):
            for j in i.winfo_children():
                j.destroy()
        self.spawn()

    def login(self):
        '''获取登录数据创建账户'''
        self.way="Microsoft"
        self.login_server=""
        self.account=""
        self.password=""
        self.server=""
        self.role = ""
        self.way=self.way_single_ver.get()
        if self.way=="Yggdrasil":
           self.login_server=self.login_server_ent.get()
           self.role = self.role_ent.get()
        self.account=self.account_ent.get()
        self.password=self.password_ent.get()
        self.server=self.server_ent.get()
        if self.way=="Yggdrasil" and not self.login_server:
            self.warning.config(text="认证服务器IP不能为空！")
        elif not self.account:
            self.warning.config(text="账号不能为空！")
        elif not self.password:
            self.warning.config(text="密码不能为空！")
        elif not self.server:
            self.warning.config(text="游戏服务器IP不能为空！")
        else:
            accounts.add([self.way,self.account,self.password,self.server,self.login_server,self.role])
            app.update_account()
            self.window.destroy()

class AccountFrame:
    '''账号启动框架类(存储账号的对象内容)'''
    def __init__(self,master,number,data):
        self.master = master
        self.frame=LabelFrame(self.master.main_frame)
        self.number=number
        self.data=data

        self.set_queue()

        self.control_window = None
        self.exe = None
        self.working = False
        self.restart_count = 0
        self.max_restart_count = 3
        self.auto_respawn = True    #立即重生
        self.auto_quit = False  #死亡退出
        self.cache_message = [] #消息缓存

        self.listen_command()   #持续监听
        self.listen_output()

        self.button()   #生成组件
        self.text()

        self.filename=num=str(self.number+1000)[1:]
        self.path_dic = {
                         "ini_path":f"config/app_data/{self.filename}/MinecraftClient.ini",
                         "exe_path":f"config/app_data/{self.filename}/MinecraftClient.exe",
                         "log_path":f"config/app_data/{self.filename}/listening.log",
                         "dir_path":f"config/app_data/{self.filename}"
                         }

        self.log = logging.getLogger(f"AccountFrame_{self.number}")
        self.log.setLevel(logging.INFO)
        
        # 动态添加 FileHandler（避免重复添加）
        if not self.log.handlers:
            handler = logging.FileHandler(
                self.path_dic["log_path"],
                mode="w",  
                encoding="utf-8",
            )
            #formatter = logging.Formatter("%(message)s")
            #handler.setFormatter(formatter)
            self.log.addHandler(handler)

    def set_queue(self):
        self.in_queue = Queue()     #通过队列与MCC进程通信
        self.out_queue = Queue()    #MCC输出
        self.get_command_queue = Queue()#接受自定义命令
        self.put_command_queue = Queue()#发送自定义命令
        self.state_queue = Queue()  #假人状态接收

    def button(self):
        self.start_button=Button(self.frame,text="启动",command=self.start)   #启动/退出按钮
        if self.working == True:
            self.start_button.config(text="退出")
        self.start_button.pack(side="right",fill="y")
        self.delete_button = Button(self.frame, text="删除", command=self.delete) #删除按钮
        self.delete_button.pack(side="right",fill="y")
        self.edit_button=Button(self.frame,text="编辑", command=self.edit)   #编辑按钮
        self.edit_button.pack(side="right",fill="y")
        self.edit_button=Button(self.frame,text="窗口", command=self.control)   #窗口按钮
        self.edit_button.pack(side="right",fill="y")

    def text(self):
        if self.data[0]=="Microsoft":
            self.account_text=Label(self.frame,text="正版账户："+str(self.data[1]))
            self.account_text.pack(anchor="w")
            self.server_text=Label(self.frame,text="游戏服务器IP："+str(self.data[3]))
            self.server_text.pack(anchor="w")
        else:
            self.account_text=Label(self.frame,text="认证服务器账户："+str(self.data[1]))
            self.account_text.pack(anchor="w")
            self.login_server_text=Label(self.frame,text="认证服务器IP："+str(self.data[4]))
            self.login_server_text.pack(anchor="w")
            self.server_text=Label(self.frame,text="游戏服务器IP："+str(self.data[3]))
            self.server_text.pack(anchor="w")
            self.role_text=Label(self.frame,text="角色名："+str(self.data[5]))
            self.role_text.pack(anchor="w")

    def start(self):
        if not self.working:
            self.start_button.config(text="退出")
            setini.login_ini(self.data,self.path_dic["ini_path"])
            if self.exe != None and self.exe.is_alive():
                print(f"[DEBUG]上一个相同子进程（{self.exe.pid}）未结束，将强制终止")
                self.close_MCC()
                #self.exe.terminate()
                #self.exe.join()
            self.set_queue()
            self.creat_process()
            self.window_print("[MCCGUI] 首次启动伊始默认不允许重连", self.log)
            self.working = True
            self.exe.start()
            if self.control_window != None and self.control_window.is_alive():
                self.control_window.start_button.config(text="退出")
                self.control_window.reco_button.config(state=NORMAL)
        else:
            self.stop()

    def stop(self):
        self.start_button.config(text="启动")
        self.restart_count = 0
        if self.working:
            self.in_queue.put("/quit",False)
        self.working = False
        self.window_print("[MCCGUI] 正在退出。。。", self.log)
        if self.control_window != None and self.control_window.is_alive():
            self.control_window.start_button.config(text="启动")
            self.control_window.reco_button.config(state=DISABLED)
            self.control_window.state_dic.update(self.control_window.default_state_dic)
            self.control_window.update_state()

    def delete(self):
        if not self.working:
            accounts.delete(self.number)
            app.update_account()
        else:
            print("[DEBUG]进程工作中无法删除！")

    def edit(self):
        if not self.working:
            self.edit_window = EditAccount(self.master, self.number, self.data)
        else:
            print("[DEBUG]进程工作中无法编辑！")

    def control(self):
        '''打开控制窗口'''
        if self.control_window != None and self.control_window.is_alive():
            self.control_window.display()
        else:
            self.control_window = None
            self.control_window = ControlWindow(self.master, self, self.in_queue, self.out_queue, self.state_queue, self.path_dic["log_path"])

    def listen_command(self):
        '''监听来自子进程的指令输出'''
        if not self.get_command_queue.empty():
            command_output = self.get_command_queue.get(False)
            if self.working:
                if command_output == "close":
                    print(f"[DEBUG]父进程（{os.getpid()}）接收到{self.data[5]}子进程（{self.exe.pid}）的反馈信号\"close\",即将自动关闭")
                    self.working = False
                    self.stop()

                elif command_output == "restart":
                    print(f"[DEBUG]父进程（{os.getpid()}）接收到{self.data[5]}子进程（{self.exe.pid}）的反馈信号\"restart\"，即将尝试重连")
                    if self.restart_count < 3:
                        self.restart()
                    else:
                        self.window_print(f"[MCCGUI] {self.data[5]}子进程（{self.exe.pid}）重连失败，即将自动关闭", self.log)
                        self.working = False
                        self.stop()

                elif command_output == "connect":
                    print(f"[DEBUG]父进程（{os.getpid()}）接收到{self.data[5]}子进程（{self.exe.pid}）的反馈信号\"connect\"")
                    if self.restart_count > 0:
                        self.restart_count = 0
                        self.window_print(f"[MCCGUI] 重连成功！重连次数已经清零{self.restart_count}/{self.max_restart_count}", self.log)

                elif command_output == "dead":
                    print(f"[DEBUG]父进程（{os.getpid()}）接收到{self.data[5]}子进程（{self.exe.pid}）的反馈信号\"respawn\"")
                    if self.auto_quit:
                        self.window_print(f"[MCCGUI] 已开启死亡退出，{self.data[5]}将重生并立即退出游戏。", self.log)
                        self.respawn()
                        self.stop()
                        


        self.frame.after(100,self.listen_command)

    def listen_output(self):
        '''监听来自MCC的消息输出并写入日志和发送给监听窗口'''
        if not self.out_queue.empty():
            output = self.out_queue.get(False)
            self.log.info(output)   #写入日志
            if self.control_window != None and self.control_window.is_alive():
                self.control_window.get_output(output)
        
        self.frame.after(10,self.listen_output)

    def update(self):
        '''刷新组件'''
        for i in self.frame.winfo_children():
            i.destroy()
        self.button()
        self.text()

    def restart(self):
        self.restart_count += 1
        if self.exe.is_alive():
            self.close_MCC()
        self.set_queue()
        self.creat_process(True)
        self.window_print(f"[MCCGUI] 正在尝试重连。。。{self.restart_count}/{self.max_restart_count}", self.log)
        self.exe.start()
        if self.control_window != None and self.control_window.is_alive():
            self.control_window.state_dic.update(self.control_window.default_state_dic)
            self.control_window.update_state()

    def respawn(self):
        if self.working:
            self.in_queue.put("/respawn")
            self.window_print(f"[MCCGUI] {self.data[5]}已重生", self.log)
    
    def send_command(self, command):
        '''向子进程发送命令'''
        self.put_command_queue.put(command, False)
        print(f"[DEBUG]主进程（{os.getpid()}）向子进程（{self.exe.pid}）发送信号“close_mcc”")

    def close_MCC(self):
        self.send_command("close_mcc")

    def creat_process(self, if_restart = False):
        self.exe = start.MCC_Process(self.path_dic, self.in_queue, self.out_queue, self.put_command_queue, self.get_command_queue, self.state_queue, self.data, if_restart)

    def window_print(self, text, log = None):
        '''输出内容到输出流、日志（如果有）和监听窗口'''
        MCCGUI_print(text, log)
        if self.control_window != None and self.control_window.is_alive():
            self.control_window.get_output(text)

class ControlWindow:
    '''控制窗口类'''
    def __init__(self, master, submaster, in_queue, out_queue, state_queue, log_path):
        self.window = Toplevel(master.window)
        self.window.title("发送消息或命令")
        self.width = 600
        self.height = 400
        self.window.geometry(f"{self.width}x{self.height}+{master.window.winfo_x() +(master.window.winfo_width()-self.width)//2}+{master.window.winfo_y()+(master.window.winfo_height()-self.height)//2}")  #窗口居中显示
        self.window.resizable(False,False)
        self.in_queue = in_queue    #输入队列
        self.out_queue = out_queue  #输出队列
        self.state_queue = state_queue #获取假人状态
        self.log_path = log_path  #日志路径
        self.master = master
        self.submaster = submaster

        self.cache_message_index = 0    #当前显示的缓存消息索引

        self.default_state_dic = {
            "alive" : None,
            "health" : None,
            "saturation" : None,
            "level" : None,
            "total_experience" : None
            }
        self.state_dic = {}
        self.state_dic.update(self.default_state_dic)

        self.spawn()
        self.bind()
        self.get_state()


    def spawn(self):
        '''生成组件'''
        self.frame()
        self.label()
        self.text()
        self.ent()
        self.button()

    def frame(self):
        '''生成框架'''
        self.io_frame = Frame(self.window) #输入/输出框架
        self.io_frame.pack(side="left", padx=5)
        self.control_frame = LabelFrame(self.window, text="控制功能", labelanchor="n") #控制功能框架
        self.control_frame.pack(anchor=NE, fill=BOTH, padx=(0,3), pady=3)
        self.bot_state_frame = LabelFrame(self.window, text="假人状态", labelanchor="n") #假人状态框架
        self.bot_state_frame.pack(anchor=SE, fill=BOTH, padx=(0,3), pady=3)

    def label(self):
        '''生成标签'''
        self.listening_text = Label(self.io_frame, text="监听窗口")
        self.listening_text.pack(side="top", padx=(5,5), pady=(2,2), fill=X)

        self.bot_alive_text = Label(self.bot_state_frame)
        self.bot_alive_text.pack(anchor=SW, pady=3)
        self.bot_health_text = Label(self.bot_state_frame)
        self.bot_health_text.pack(anchor=SW, pady=3)
        self.bot_saturation_text = Label(self.bot_state_frame)
        self.bot_saturation_text.pack(anchor=SW, pady=3)
        self.bot_level_text = Label(self.bot_state_frame)
        self.bot_level_text.pack(anchor=SW, pady=3)
        self.bot_total_experience_text = Label(self.bot_state_frame)
        self.bot_total_experience_text.pack(anchor=SW, pady=3)
        self.update_state() #设置状态文本

    def text(self):
        '''生成大型文本消息框'''
        self.listening_scrolltext = tkinter.scrolledtext.ScrolledText(self.io_frame, state=NORMAL, width=65, height=23)
        self.listening_scrolltext.pack()
        log_file = open(self.log_path, "r", encoding="utf-8")
        log_text_list = log_file.readlines()
        for text in log_text_list:
            self.listening_scrolltext.insert(END, text)    #去掉换行符
        self.listening_scrolltext.config(state=DISABLED)    #设置为只读（用户不可写入）
        self.listening_scrolltext.see(END)

    def ent(self):
        '''生成文本框'''
        self.text_ent = Entry(self.io_frame)
        self.text_ent.pack(anchor=SW, pady=(5,0), padx=(0,15), fill=X)
        self.text_ent.focus()

    def button(self):
        '''生成按钮'''
        self.send_button = Button(self.io_frame, text="发送", command=self.send_message)
        self.send_button.pack(expand=True, fill=Y, ipadx=20,pady=5)

        self.start_button = Button(self.control_frame, text="启动", command=self.submaster.start)
        if self.submaster.working:
            self.start_button.config(text="退出")
        self.start_button.pack(fill=X, ipadx=30, padx=3, pady=3)

        self.reco_button = Button(self.control_frame, text="重连", command=self.submaster.restart, state=DISABLED)
        if self.submaster.working:
            self.reco_button.config(state=NORMAL)
        self.reco_button.pack(fill=X, ipadx=30, padx=3, pady=3)

        self.respwan_button = Button(self.control_frame, text="重生", command=self.submaster.respawn, state=DISABLED)
        if self.state_dic["alive"]:
            self.respawn_button.config(state=NORMAL)
        self.respwan_button.pack(fill=X, ipadx=30, padx=3, pady=(3,6))

    def bind(self):
        '''事件绑定'''
        self.window.bind("<Return>", self.send_message)
        self.window.bind("<Up>", self.read_cache)
        self.window.bind("<Down>", self.read_cache)

    def send_message(self, event = None):
        '''发送消息'''
        text = self.text_ent.get()
        if event:
            print("[DEBUG]Enter键按下")
        if text and self.submaster.working:
            send_text = "/send "+ text
            self.submaster.cache_message.append(text)
            self.cache_message_index = 0
            self.in_queue.put(send_text, False)
            self.text_ent.delete(0, END)
            self.listening_scrolltext.see(END)
            print(self.submaster.cache_message)

    def get_output(self, output):
        '''接收监听内容并显示'''
        buttom_display = False
        top, buttom = self.listening_scrolltext.yview()
        if buttom == 1:
            buttom_display = True
        self.listening_scrolltext.config(state=NORMAL)
        self.listening_scrolltext.insert(END, output + "\n")
        self.listening_scrolltext.config(state=DISABLED)
        if buttom_display:
            self.listening_scrolltext.see(END)

    def display(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
        self.text_ent.focus()

    def is_alive(self):
        return self.window.winfo_exists()

    def get_state(self):
        '''获取假人状态并显示'''
        if not self.state_queue.empty():
            self.state_dic.update(self.state_queue.get(False))
            self.update_state()
            if self.state_dic["alive"]:
                self.respwan_button.config(state=DISABLED)
            else:
                self.respwan_button.config(state=NORMAL)
        
        self.window.after(100, self.get_state)

    def update_state(self):
        '''更新假人状态显示'''
        self.bot_alive_text.config(text=f"存活状态：{"未知" if self.state_dic["alive"] == None else("存活" if self.state_dic["alive"] else "死亡")}")
        self.bot_health_text.config(text=f"生命值：{self.state_dic["health"]}")
        self.bot_saturation_text.config(text=f"饥饿值：{self.state_dic["saturation"]}")
        self.bot_level_text.config(text=f"经验等级：{self.state_dic["level"]}")
        self.bot_total_experience_text.config(text=f"经验值：{self.state_dic["total_experience"]}")

    def read_cache(self, event):
        '''按下↑或↓显示缓存消息'''
        if event.keysym == "Up":
            print("UP键被按下")
            if self.cache_message_index >= 1 - len(self.submaster.cache_message):
                self.cache_message_index -= 1
            if len(self.submaster.cache_message):
                self.text_ent.delete(0, END)
                self.text_ent.insert(0, self.submaster.cache_message[self.cache_message_index])
        elif event.keysym == "Down":
            print("DOWN键被按下")
            if self.cache_message_index < -1:
                self.cache_message_index += 1
            if len(self.submaster.cache_message):
                self.text_ent.delete(0, END)
                self.text_ent.insert(0, self.submaster.cache_message[self.cache_message_index])
            

class EditAccount:
    '''编辑账户窗口类'''
    def __init__(self, master, number, data):
        self.number = number
        self.way = data[0]
        self.account = data[1]
        self.password = data[2]
        self.server = data[3]
        self.login_server = data[4]
        self.role = data[5]

        self.window = Toplevel(master.window)
        self.window.title("编辑账户")
        self.width=300
        self.height=230
        self.window.resizable(False,False)
        self.window.grab_set()      #禁用父窗口
        self.window.geometry(f"{self.width}x{self.height}+{master.window.winfo_x() +(master.window.winfo_width()-self.width)//2}+{master.window.winfo_y()+(master.window.winfo_height()-self.height)//2}")  #窗口居中显示
        self.frame()
        self.spawn()

    def spawn(self):
        '''生成组件(不包括框架)'''
        self.ent()
        self.button()
        self.text()

    def text(self):
        '''文本消息'''
        self.warning=Label(self.frame3,fg="red")
        self.warning.pack()

    def frame(self):
        '''框架'''
        self.frame1=Frame(self.window) #装登录方式
        self.frame1.pack(pady=10)
        self.frame2=Frame(self.window) #装账密
        self.frame2.pack(pady=0)
        self.frame3=Frame(self.window) #装保存按钮
        self.frame3.pack(pady=10)

    def ent(self):
        '''选择器、文本框'''
        self.row=0

        self.way_label=Label(self.frame1,text="登录方式:")  #登录方式
        self.way_label.grid(row=self.row,column=0)
        if self.way == "Microsoft":
            self.way_single=Radiobutton(self.frame1,text="正版账户")
            self.way_single.grid(row=self.row,column=1)
        elif self.way == "Yggdrasil":
            self.way_single=Radiobutton(self.frame1,text="第三方认证账户")
            self.way_single.grid(row=self.row,column=2)
        self.row+=1

        self.account_label=Label(self.frame2,text="账号:") #账号
        self.account_label.grid(row=self.row,column=0)
        self.account_ent=Entry(self.frame2)
        self.account_ent.insert(0, self.account)
        self.account_ent.grid(row=self.row,column=1)
        self.row+=1

        self.password_label=Label(self.frame2,text="密码:") #密码
        self.password_label.grid(row=self.row,column=0)
        self.password_ent=Entry(self.frame2,show="*")
        self.password_ent.insert(0, self.password)
        self.password_ent.grid(row=self.row,column=1)
        self.row+=1

        self.server_label=Label(self.frame2,text="游戏服务器IPIP:") #服务器IP
        self.server_label.grid(row=self.row,column=0)
        self.server_ent=Entry(self.frame2)
        self.server_ent.insert(0, self.server)
        self.server_ent.grid(row=self.row,column=1)
        self.row+=1

        if self.way =="Yggdrasil": 
            self.login_server_label=Label(self.frame2,text="认证服务器IP")  #认证服务器
            self.login_server_label.grid(row=self.row,column=0)
            self.login_server_ent=Entry(self.frame2)
            self.login_server_ent.insert(0, self.login_server)
            self.login_server_ent.grid(row=self.row,column=1)
            self.row+=1

            self.role_label = Label(self.frame2, text = "角色名")    #登录角色
            self.role_label.grid(row=self.row,column=0)
            self.role_ent=Entry(self.frame2)
            self.role_ent.insert(0, self.role)
            self.role_ent.grid(row=self.row,column=1)
            self.row+=1

    def button(self):
        '''按钮'''
        self.login_button=Button(self.frame3,text="保存",command=self.save) #保存按钮
        self.login_button.pack()

    def update(self):
        '''刷新组件'''
        for i in (self.frame1,self.frame2,self.frame3):
            for j in i.winfo_children():
                j.destroy()
        self.spawn()

    def save(self):
        '''获取登录数据创建账户'''
        if self.way=="Yggdrasil":
           self.login_server=self.login_server_ent.get()
           self.role = self.role_ent.get()
        self.account=self.account_ent.get()
        self.password=self.password_ent.get()
        self.server=self.server_ent.get()
        if self.way=="Yggdrasil" and not self.login_server:
            self.warning.config(text="认证服务器IP不能为空！")
        elif not self.account:
            self.warning.config(text="账号不能为空！")
        elif not self.password:
            self.warning.config(text="密码不能为空！")
        elif not self.server:
            self.warning.config(text="游戏服务器IP不能为空！")
        else:
            accounts.set(self.number, [self.way,self.account,self.password,self.server,self.login_server,self.role])
            app.update_account()
            self.window.destroy()

def creat_user_file(filename,user_data):
    if os.path.isdir(f"user/{filename}"):
        shutil.rmtree(f"user/{filename}",ignore_errors=False,onerror=None)
    shutil.copytree("config/app_default",f"config/app_data/{filename}")
    print(f"[DEBUG]已生成{filename}")

def MCCGUI_print(text, log = None):
    '''同时输出到输出流和日志(如果有的话)'''
    print(text)
    if log != None:
        log.info(text)

def run():
    return MCC_GUI()

if __name__=="__main__":
    print(f"主进程MCCGUI_v{version} {"for MangoCraft" if MangoCraft else ""}（{os.getpid()}）已启动。")
    freeze_support()
    app = run()

    mainloop()
