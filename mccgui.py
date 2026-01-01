from re import M, sub
import time
from tkinter import *
import tkinter.scrolledtext
import os
from multiprocessing import Queue, freeze_support
from threading import Thread
import logging
import sys
import ping3


from databace import user_data
import set_toml
import start
from __version__ import __version__, MangoCraft
from utils import *
from display_text import display_text

#代码文件名
FILE_NAME = os.path.basename(__file__)  

USER_DATA_COLUMNS = list(user_data.columns())
USER_DATA_COLUMNS.pop(0)                #去掉id字段的字段名的列表

class MCC_GUI():
    '''主窗口类'''
    def __init__(self):
        global SCREEN_WIDTH,SCREEN_HEIGHT #窗口
        self.window=Tk()
        self.window.title(f"MCC GUI 可交互式工具 v{__version__}{" 芒果方块粉丝服定制版" if MangoCraft else ""}")
        self.window.iconbitmap("bin/AppIcon.ico")
        self.window.protocol("WM_DELETE_WINDOW", self.close)    #关闭窗口后强制关闭主进程
        self.WIDTH=800
        self.HEIGHT=600
        SCREEN_WIDTH=self.window.winfo_screenwidth()
        SCREEN_HEIGHT=self.window.winfo_screenheight()
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{(SCREEN_WIDTH-self.WIDTH)//2}+{(SCREEN_HEIGHT-self.HEIGHT)//3}")     #居中显示
        self.window.resizable(False,False)
        self.canvas=Canvas(self.window,width=self.WIDTH, height=self.HEIGHT)
        self.main_frame=Frame(self.canvas,width=self.WIDTH)
        self.canvas.create_window((0,0),window=self.main_frame,anchor="nw",width=self.WIDTH) #创建可以滚动的框架
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
        self.control_frame = Frame(self.main_frame)
        self.control_frame.pack(fill=X, padx=10)
        self.add_account_button=Button(self.control_frame,text="添加账户",command=self.open_add_account_window)
        self.add_account_button.pack(side=LEFT, ipadx=5, ipady=2, pady=5)
        self.update_ping_button = Button(self.control_frame, text="刷新", command=self.ping)
        self.update_ping_button.pack(side=RIGHT, pady=5)

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
        self.count=len(user_data)
        print(f"[DEBUG:{FILE_NAME}]账号数量",self.count)
        for data_id, data_dic in user_data.get_all():
            self.verification(data_dic, data_id)
            self.accounts.append(AccountFrame(self, data_id, data_dic))
            self.accounts[-1].frame.pack(fill="both", padx=4)
            print(f"[DEBUG:{FILE_NAME}]账户id={data_id}已生成")

    def update_account(self):
        '''更新账户列表'''
        self.show_accounts()

    def verification(self,user_data_dic,data_id):
        '''校验并修复文件'''
        num = str(data_id+1000)[1:]
        flag = False
        if os.path.isdir(f"config/app_data/{num}"):
            if os.path.isfile(f"config/app_data/{num}/MinecraftClient.exe"):
                flag=True
        if not flag:
            creat_user_file(num)
    
    def close(self):
        print(f"用户关闭主窗口，主进程以及所有子进程都将将强制关闭！")
        self.window.destroy()
        for account in self.accounts:
            if account.exe != None:
                account.close_MCC()
        sys.exit(0)

    def ping(self):
        '''对各个账户服务器进行连通性测试'''
        for account in self.accounts:
            account.ping_update()


class AddAccount:
    '''添加账户窗口类'''
    def __init__(self, master):
        self.window = Toplevel(master.window)
        self.window.title("添加账户")
        self.WIDTH = 450
        self.HEIGHT = 300
        self.ENTRY_WIDTH = 30
        self.PORT_ENTRY_WIDTH = 5
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.window.resizable(False,False)
        self.window.grab_set()      #禁用父窗口
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{master.window.winfo_x()+(master.window.winfo_width()-self.WIDTH)//2}+{master.window.winfo_y()+(master.window.winfo_height()-self.HEIGHT)//2}")  #窗口居中显示
        self.master = master
        
        self.init_single()
        self.frame()
        self.spawn()

    def init_single(self):
        '''初始化登录方式单选建'''
        self.account_type_single_ver = StringVar() #登录方式选项初始化
        self.account_type_single_ver.set("microsoft")
        if MangoCraft:          #芒果方块定制
            self.account_type_single_ver.set("yggdrasil")

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

        self.account_type_label=Label(self.frame1,text="登录方式:", anchor=E)  #登录方式
        self.account_type_label.grid(row=self.row,column=0, pady = 5)
        self.account_type1_single=Radiobutton(self.frame1,text="正版账户",variable=self.account_type_single_ver,value="microsoft",command=self.update)
        self.account_type1_single.grid(row=self.row,column=1, pady = 5)
        self.account_type2_single=Radiobutton(self.frame1,text="第三方认证账户",variable=self.account_type_single_ver,value="yggdrasil",command=self.update)
        self.account_type2_single.grid(row=self.row,column=2, pady = 5)

        self.row+=1

        self.account_label=Label(self.frame2,text="账号:", anchor=E) #账号
        self.account_label.grid(row=self.row,column=0, pady = 5)
        self.account_ent=Entry(self.frame2, width=self.ENTRY_WIDTH)
        self.account_ent.grid(row=self.row,column=1, pady = 5)

        self.row+=1

        self.password_label=Label(self.frame2,text="密码:", anchor=E) #密码
        self.password_label.grid(row=self.row,column=0, pady = 5)
        self.password_ent=Entry(self.frame2, show="*", width=self.ENTRY_WIDTH)
        self.password_ent.grid(row=self.row,column=1, pady = 5)

        self.row+=1

        self.game_server_ip_label=Label(self.frame2,text="游戏服务器IP:", anchor=E) #服务器IP
        self.game_server_ip_label.grid(row=self.row,column=0, pady = 5)
        self.game_server_ip_ent=Entry(self.frame2, width=self.ENTRY_WIDTH)
        self.game_server_ip_ent.grid(row=self.row,column=1, pady = 5)
        

        self.game_server_port_label=Label(self.frame2,text="端口:", anchor=E) #服务器端口
        self.game_server_port_label.grid(row=self.row, column=2, pady=5, padx=5)
        self.game_server_port_ent=Entry(self.frame2, width=self.PORT_ENTRY_WIDTH)
        self.game_server_port_ent.grid(row=self.row, column=3, pady = 5)

        self.row+=1

        if MangoCraft and self.__class__.__name__ == "AddAccount":   #芒果方块定制
            self.game_server_ip_ent.insert(0, "bot.server.mangocraft.cn")
            self.game_server_port_ent.insert(0, "8080")

        if self.account_type_single_ver.get()=="yggdrasil": 
            self.login_server_ip_label=Label(self.frame2,text="认证服务器IP:", anchor=E)  #认证服务器
            self.login_server_ip_label.grid(row=self.row,column=0, pady = 5)
            self.login_server_ip_ent=Entry(self.frame2, width=self.ENTRY_WIDTH)
            self.login_server_ip_ent.grid(row=self.row,column=1, pady = 5)   
            

            self.login_server_port_label=Label(self.frame2,text="端口:", anchor=E) #认证服务器端口
            self.login_server_port_label.grid(row=self.row, column=2, pady = 5)
            self.login_server_port_ent=Entry(self.frame2, width=self.PORT_ENTRY_WIDTH)
            self.login_server_port_ent.grid(row=self.row, column=3, pady = 5)

            if MangoCraft and self.__class__.__name__ == "AddAccount":   #芒果方块定制
                self.login_server_ip_ent.insert(0, "skin.prinzeugen.net")   
                self.login_server_port_ent.insert(0, "443") 

            self.row+=1

            self.role_name_label = Label(self.frame2, text = "角色名:", anchor=E)    #登录角色
            self.role_name_label.grid(row=self.row,column=0, pady = 5)
            self.role_name_ent=Entry(self.frame2, width=self.ENTRY_WIDTH)
            self.role_name_ent.grid(row=self.row,column=1, pady = 5)

            self.row+=1

    def button(self):
        '''按钮'''
        self.login_button=Button(self.frame3,text="创建账户",command=self.login) #登录按钮
        self.login_button.pack(ipadx=5, ipady=3, pady=(3,0))

    def update(self):
        '''刷新组件'''
        for i in (self.frame1,self.frame2,self.frame3):
            for j in i.winfo_children():
                j.destroy()
        self.spawn()

    def login(self):
        '''获取登录数据创建账户'''
        account = ""                #账号
        password = ""               #密码
        game_server_ip = ""         #游戏服务器域名或IP
        game_server_port = ""       #游戏服务器端口
        login_server_ip = ""        #认证服务器域名或IP
        login_server_port = ""      #认证服务器端口
        role_name = ""              #角色名字（适用于多角色账户，单角色可不填写）
        account_type = ""                 #登录方式（微软、离线、第三方）

        account_type=self.account_type_single_ver.get()             #读取输入同时验证是否留空

        if account_type == "yggdrasil":
           login_server_ip = self.login_server_ip_ent.get()
           login_server_port = self.login_server_port_ent.get()
           role_name = self.role_name_ent.get()

        account = self.account_ent.get()
        password = self.password_ent.get()
        game_server_ip = self.game_server_ip_ent.get()
        game_server_port = self.game_server_port_ent.get()

        if account_type=="yggdrasil" and not login_server_ip:
            self.warning.config(text="认证服务器IP不能为空！")
        elif not account:
            self.warning.config(text="账号不能为空！")
        elif not password:
            self.warning.config(text="密码不能为空！")
        elif not game_server_ip:
            self.warning.config(text="游戏服务器IP不能为空！")
        else:                                        #数据完整，可以写入
            new_data_values = [
                account, 
                password, 
                game_server_ip, 
                game_server_port,
                login_server_ip,
                login_server_port,
                role_name,
                account_type
                ]
            new_user_data_dic = dict(zip(USER_DATA_COLUMNS, new_data_values))   #新账户数据
            self.run(new_user_data_dic)
            self.master.update_account()
            self.window.destroy()

    def run(self, new_user_data_dic):
        '''添加账户（继承后可以重写）'''
        user_data.add(new_user_data_dic)


class EditAccount(AddAccount):
    '''编辑账户窗口类（继承自添加账户窗口）'''
    def __init__(self, master, data_id, data):
        self.id = data_id
        self.account = data["account"]
        self.password = data["password"]
        self.game_server_ip = data["game_server_ip"]
        self.game_server_port = data["game_server_port"]
        self.login_server_ip = data["login_server_ip"]
        self.login_server_port = data["login_server_port"]
        self.role_name = data["role_name"]
        self.account_type = data["account_type"]

        AddAccount.__init__(self, master)

        self.account_type_single_ver.set(self.account_type)
        self.window.title("编辑账户")
    
    def init_single(self):
        '''初始化登录方式单选建（重写）'''
        self.account_type_single_ver = StringVar() #登录方式选项初始化
        self.account_type_single_ver.set(self.account_type)

    def ent(self):
        '''选择器、文本框（增加）'''
        AddAccount.ent(self)
        if self.account_type == "microsoft":
            self.account_type1_single.grid(row=0,column=1)
        elif self.account_type == "yggdrasil":
            self.account_type2_single.grid(row=0,column=1)

        self.account_ent.insert(0, self.account)
        self.password_ent.insert(0, self.password)
        self.game_server_ip_ent.insert(0, self.game_server_ip)
        self.game_server_port_ent.insert(0, self.game_server_port)

        if self.account_type =="yggdrasil": 
            self.login_server_ip_ent.insert(0, self.login_server_ip)
            self.login_server_port_ent.insert(0, self.login_server_port)
            self.role_name_ent.insert(0, self.role_name)

    def button(self):
        '''按钮（修改）'''
        AddAccount.button(self)
        self.login_button.config(text="保存账户")

    def run(self, new_user_data_dic):
        '''提交修改账户（重写）'''
        user_data.update(self.id, new_user_data_dic)


class AccountFrame:
    '''账号启动框架类(存储账号的对象内容)'''
    def __init__(self, master, data_id, data):
        self.master = master
        self.frame = LabelFrame(self.master.main_frame)
        self.id = data_id
        self.data = data
        self.control_window = None
        self.exe = None
        self.working = False
        self.restart_count = 0
        self.max_restart_count = 3
        self.auto_respawn = True    #立即重生
        self.auto_quit = False  #死亡退出
        self.cache_message = [] #消息缓存

        self.set_queue()

        self.listen_command()   #持续监听
        self.listen_output()

        self.button()   #生成组件
        self.text()

        self.filename=num=str(self.id+1000)[1:]
        self.path_dic = {
                         "ini_path":f"config/app_data/{self.filename}/MinecraftClient.ini",
                         "exe_path":f"config/app_data/{self.filename}/MinecraftClient.exe",
                         "log_path":f"config/app_data/{self.filename}/listening.log",
                         "dir_path":f"config/app_data/{self.filename}"
                         }

        self.log = logging.getLogger(f"AccountFrame_{self.id}")
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

        self.ping_thread = Thread(name=f"{self.data["role_name"]}-ping_thread", target=self.ping) #连通性测试线程
        self.ping_thread.start()

    def set_queue(self):
        self.in_queue = Queue()             #通过队列与MCC进程通信
        self.out_queue = Queue()            #MCC输出
        self.get_command_queue = Queue()    #接受自定义命令
        self.put_command_queue = Queue()    #发送自定义命令
        self.state_queue = Queue()          #假人状态接收

        if self.control_window != None:     #向控制窗口同步新的通信队列
            self.control_window.in_queue = self.in_queue
            self.control_window.out_queue = self.out_queue
            self.control_window.state_queue = self.state_queue

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
        if self.data["account_type"]=="microsoft":
            self.account_text=Label(self.frame,text="正版账户：" + self.data["account"])
            self.account_text.pack(anchor="w")
            self.game_server_ip_text=Label(self.frame,text="游戏服务器IP：" + self.data["game_server_ip"])
            self.game_server_ip_text.pack(anchor="w")
        else:
            self.account_text=Label(self.frame,text="认证服务器账户："+ self.data["account"])
            self.account_text.pack(anchor="w")
            self.login_server_ip_text=Label(self.frame,text="认证服务器IP：" + self.data["login_server_ip"])
            self.login_server_ip_text.pack(anchor="w")
            self.game_server_ip_text=Label(self.frame,text="游戏服务器IP：" + self.data["game_server_ip"])
            self.game_server_ip_text.pack(anchor="w")
            self.role_name_text=Label(self.frame,text="角色名：" + self.data["role_name"])
            self.role_name_text.pack(anchor="w")

    def start(self):
        if not self.working:
            self.start_button.config(text="退出")
            set_toml.set_user_data(self.data, self.path_dic["ini_path"])
            if self.exe != None and self.exe.is_alive():
                print(f"[DEBUG:{FILE_NAME}]上一个相同子进程（{self.exe.pid}）未结束，将强制终止")
                self.close_MCC()
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
            user_data.delete(self.id)
            self.master.update_account()
        else:
            print(f"[DEBUG:{FILE_NAME}]进程工作中无法删除！")

    def edit(self):
        if not self.working:
            self.edit_window = EditAccount(self.master, self.id, self.data)
        else:
            print(f"[DEBUG:{FILE_NAME}]进程工作中无法编辑！")

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
                    print(f"[DEBUG:{FILE_NAME}]父进程（{os.getpid()}）接收到{self.data["role_name"]}子进程（{self.exe.pid}）的反馈信号\"close\",即将自动关闭")
                    self.working = False
                    self.stop()

                elif command_output == "restart":
                    print(f"[DEBUG:{FILE_NAME}]父进程（{os.getpid()}）接收到{self.data["role_name"]}子进程（{self.exe.pid}）的反馈信号\"restart\"，即将尝试重连")
                    if self.restart_count < 3:
                        self.restart()
                    else:
                        self.window_print(f"[MCCGUI] {self.data["role_name"]}子进程（{self.exe.pid}）重连失败，即将自动关闭", self.log)
                        self.working = False
                        self.stop()

                elif command_output == "connect":
                    print(f"[DEBUG:{FILE_NAME}]父进程（{os.getpid()}）接收到{self.data["role_name"]}子进程（{self.exe.pid}）的反馈信号\"connect\"")
                    if self.restart_count > 0:
                        self.restart_count = 0
                        self.window_print(f"[MCCGUI] 重连成功！重连次数已经清零{self.restart_count}/{self.max_restart_count}", self.log)

                elif command_output == "dead":
                    print(f"[DEBUG:{FILE_NAME}]父进程（{os.getpid()}）接收到{self.data["role_name"]}子进程（{self.exe.pid}）的反馈信号\"respawn\"")
                    if self.auto_quit:
                        self.window_print(f"[MCCGUI] 已开启死亡退出，{self.data["role_name"]}将重生并立即退出游戏。", self.log)
                        self.respawn()
                        self.stop()

                elif command_output == "oauth20":
                    print(f"[DEBUG:{FILE_NAME}]父进程（{os.getpid()}）接收到{self.data["role_name"]}子进程（{self.exe.pid}）的反馈信号\"oauth20\"")
                    self.control()
                    self.control_window.open_oauth20_window()
                        
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
            self.window_print(f"[MCCGUI] {self.data["role_name"]}已重生", self.log)
    
    def send_command(self, command):
        '''向子进程发送命令'''
        self.put_command_queue.put(command, False)
        print(f"[DEBUG:{FILE_NAME}]主进程（{os.getpid()}）向子进程（{self.exe.pid}）发送信号“close_mcc”")

    def close_MCC(self):
        self.send_command("close_mcc")

    def creat_process(self, if_restart = False):
        self.exe = start.MCC_Process(self.path_dic, self.in_queue, self.out_queue, self.put_command_queue, self.get_command_queue, self.state_queue, self.data, if_restart)

    def window_print(self, text, log = None):
        '''输出内容到输出流、日志（如果有）和监听窗口'''
        MCCGUI_print(text, log)
        if self.control_window != None and self.control_window.is_alive():
            self.control_window.get_output(text)

    def ping(self):
        '''连通性测试'''
        timeout = 5

        try:
            self.game_server_daley = ping3.ping(self.data["game_server_ip"], timeout=timeout)    #单位：秒
        except Exception as e:
            self.login_server_daley = False
            print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}连通性测试失败，报错：{e}")

        if self.game_server_daley:
            print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}游戏服务器延迟（{self.data["game_server_ip"]}）：{self.game_server_daley * 1000:.2f}ms")
            self.game_server_daley_display = str(int(self.game_server_daley * 1000)) + "ms"
        elif self.game_server_daley == False:
            print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}游戏服务器无法连接")
            self.game_server_daley_display = "未知的主机"
        elif self.game_server_daley == None:
            print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}游戏服务器连接超时")
            self.game_server_daley_display = "连接超时"
        
        if self.data["account_type"] == "yggdrasil":

            try:
                self.login_server_daley = ping3.ping(self.data["login_server_ip"], timeout=timeout)
            except Exception as e:
                self.login_server_daley = False
                print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}连通性测试失败，报错：{e}")

            if self.login_server_daley:
                print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}认证服务器延迟（{self.data["login_server_ip"]}）：{self.login_server_daley * 1000:.2f}ms")
                self.login_server_daley_display = str(int(self.login_server_daley * 1000)) + "ms"
            elif self.login_server_daley == False:
                print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}认证服务器无法连接")
                self.login_server_daley_display = "未知的主机"
            elif self.login_server_daley == None:
                print(f"[DEBUG:{FILE_NAME}]{self.data["role_name"]}认证服务器连接超时")
                self.login_server_daley_display = "连接超时"
        
        self.ping_display()

    def ping_display(self):
        self.game_server_ip_text.config(text=f"游戏服务器IP：{str(self.data["game_server_ip"])} \t延迟：{self.game_server_daley_display}")
        if self.data["account_type"] == "yggdrasil":
            self.login_server_ip_text.config(text=f"认证服务器IP：{str(self.data["login_server_ip"])} \t\t延迟：{self.login_server_daley_display}")
        
    def ping_update(self):
        self.ping_thread = Thread(name=f"{self.data["role_name"]}-ping_thread", target=self.ping)  #连通性测试线程
        self.ping_thread.start()


class ControlWindow:
    '''控制窗口类'''
    def __init__(self, master, submaster, in_queue, out_queue, state_queue, log_path):
        self.window = Toplevel(master.window)
        self.window.title("发送消息或命令")
        self.WIDTH = 600
        self.HEIGHT = 400
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{master.window.winfo_x() +(master.window.winfo_width()-self.WIDTH)//2}+{master.window.winfo_y()+(master.window.winfo_height()-self.HEIGHT)//2}")  #窗口居中显示
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
        self.listening_scrolltext = tkinter.scrolledtext.ScrolledText(self.io_frame, state=NORMAL, width=65, height=23, bg="black", fg="white")
        self.listening_scrolltext.pack()
        log_file = open(self.log_path, "r", encoding="utf-8")
        log_text_list = log_file.readlines()
        for text in log_text_list:
            display_text(text.strip(), self.listening_scrolltext)    #去掉换行符
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
            print(f"[DEBUG:{FILE_NAME}]Enter键按下")
        if text and self.submaster.working:
            send_text = text
            self.submaster.cache_message.append(text)
            self.cache_message_index = 0
            self.in_queue.put("/send " + send_text, False)
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
        display_text(output, self.listening_scrolltext)
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
        
        #print(self.submaster.data["role_name"] ,self.state_dic)
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
            print("[DUBUG]UP键被按下")
            if self.cache_message_index >= 1 - len(self.submaster.cache_message):
                self.cache_message_index -= 1
            if len(self.submaster.cache_message):
                self.text_ent.delete(0, END)
                self.text_ent.insert(0, self.submaster.cache_message[self.cache_message_index])
        elif event.keysym == "Down":
            print(f"[DEBUG:{FILE_NAME}]DOWN键被按下")
            if self.cache_message_index < -1:
                self.cache_message_index += 1
            if len(self.submaster.cache_message):
                self.text_ent.delete(0, END)
                self.text_ent.insert(0, self.submaster.cache_message[self.cache_message_index])

    def open_oauth20_window(self):
        '''打开OAuth2.0令牌登录口令接收窗口'''
        self.oauth20_window = OAuth20Window(self, self.in_queue)

class OAuth20Window:
    '''OAuth2.0令牌登录口令接收窗口类'''
    def __init__(self, master, queue):
        self.window = Toplevel(master.window)
        self.window.title("输入口令内容以登录")
        self.WIDTH = 220
        self.HEIGHT = 130
        master.window.update()
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{master.window.winfo_x() +(master.window.winfo_width()-self.WIDTH)//2}+{master.window.winfo_y()+(master.window.winfo_height()-self.HEIGHT)//2}")  #窗口居中显示
        self.window.grab_set()
        self.window.resizable(False,False)

        self.queue = queue

        self.spawn()

    def spawn(self):
        self.init_lable()
        self.display()
    
    def init_lable(self):
        '''初始化组件'''
        self.ent()
        self.lable()
        self.button()

    def display(self):
        '''显示组件'''
        self.text_lable.pack()
        self.code_ent.pack()
        self.send_button.pack()

    def ent(self):
        '''文本框'''
        self.code_ent = Entry(self.window)

    def lable(self):
        '''普通组件'''
        self.text_lable = Label(self.window, text="请输入在浏览器登录正版账户后\n由MCC官网提供的口令码：")

    def button(self):
        '''按钮'''
        self.send_button = Button(self.window, text="确认", command=self.send_code)

    def send_code(self):
        '''发送口令'''
        code = self.code_ent.get()
        if code:
            self.queue.put(code, False)
            self.window.destroy()
        




def run():
    return MCC_GUI()


