import os
from tkinter import  *
from tkinter.scrolledtext import ScrolledText
from unittest import enterModuleContext

from databace import shortcut_cmd_data

#代码文件名
FILE_NAME = os.path.basename(__file__)


class ShortcutCommandsGUI:
    '''快捷指令前端界面实现'''
    def __init__(self, backend, master = None):
        self.master = master
        self.WIDTH = 500
        self.HEIGHT = 350
        self._init_window()
        self._init_widgets()
        self._display()

        self.add_cmd_window = None

    def _init_window(self):
        '''初始化窗口'''
        if __name__ == "__main__":
            self.window = Tk()
            self.window.title("快捷指令管理 - 测试")
            SCREEN_WIDTH=self.window.winfo_screenwidth()
            SCREEN_HEIGHT=self.window.winfo_screenheight()
            self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{(SCREEN_WIDTH-self.WIDTH)//2}+{(SCREEN_HEIGHT-self.HEIGHT)//3}")     #居中显示

        else:
            self.window = Toplevel()
            self.window.title("快捷指令管理")
            self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.master.window.winfo_x()+(self.master.window.winfo_width()-self.WIDTH)//2}+{self.master.window.winfo_y()+(self.master.window.winfo_height()-self.HEIGHT)//2}")  #窗口居中显示
        
        self.window.resizable(False,False)

    def _init_widgets(self):
        '''初始化控件'''
        self.control_frame = Frame(self.window) #控制区域，包括添加等
        self.cmds_frame = Frame(self.window)    #快捷指令区域

        self.add_cmd_button = Button(self.control_frame, text="添加快捷指令", command=self._on_add_cmd_button)
        
        self.short_cmd_list = []
        for cmd_id, cmd_data in shortcut_cmd_data.get_all():
            self.short_cmd_list.append(ShortCmdFrame(cmd_data, cmd_id, self))
            
    def _on_add_cmd_button(self):
        '''打开添加账户窗口'''
        self.add_cmd_window = AddCmdWindow(self)


    def _display(self):
        '''显示窗口'''
        self.control_frame.pack(pady=(5,0))
        self.cmds_frame.pack(fill=BOTH)

        self.add_cmd_button.pack()
        
        for cmd in self.short_cmd_list:
            cmd.display()



class ShortCmdFrame:
        '''快捷指令框架类'''
        def __init__(self, cmd_data, cmd_id, master):
            self.cmd_list = cmd_data["cmd_content"].splitlines()
            self.cmd_name = cmd_data["cmd_name"]
            self.cmd_type = cmd_data["cmd_type"]
            self.id = cmd_id
            self.frame = LabelFrame(master.cmds_frame)
            self._init_widgets()

        def _init_widgets(self):
            '''初始化控件'''
            self.text_frame = Frame(self.frame)
            self.button_frame = Frame(self.frame)

            self.cmd_name_text = Label(self.text_frame, text=f"{"简单" if self.cmd_type == "simple" else "复杂"}快捷指令：{self.cmd_name}")

            self.edit_button = Button(self.button_frame, text="编辑")
            self.delete_button = Button(self.button_frame, text="删除")

        def display(self):
            '''显示组件'''
            self.frame.pack(fill=X, anchor=W, padx=10, pady=5)
            self.text_frame.pack(side=LEFT)
            self.button_frame.pack(side=RIGHT, fill=Y)

            self.cmd_name_text.pack(anchor=W, fill=Y)
            
            self.edit_button.pack(side=RIGHT, fill=Y)
            self.delete_button.pack(side=RIGHT, fill=Y)

class AddCmdWindow:
    '''添加快捷指令窗口'''
    def __init__(self, master):
        self.master = master
        self.WIDTH = 350
        self.HEIGHT = 270

        self._init_window()
        self._init_widgets()
        self._display()

    def is_alive(self):
        return self.window.winfo_exists()

    def _init_window(self):
        '''初始化窗口'''
        self.window = Toplevel(self.master.window)
        self.window.title("添加快捷指令")
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.master.window.winfo_x()+(self.master.window.winfo_width()-self.WIDTH)//2}+{self.master.window.winfo_y()+(self.master.window.winfo_height()-self.HEIGHT)//2}")  #窗口居中显示
        self.window.grab_set()
        self.window.resizable(False, False)

    def _init_widgets(self):
        '''初始化控件'''
        self.type_frame = Frame(self.window)    #类型选择框架
        self.name_frame = Frame(self.window)    #快捷指令名称框架
        self.cmd_frame = Frame(self.window)     #快捷指令内容框架
        self.save_frame = Frame(self.window)    #保存框架

        self.type_text = Label(self.type_frame, text="快捷指令类型：")
        self.type_single_var = StringVar()
        self.type_single_var.set("simple")
        self.type_simple_single = Radiobutton(self.type_frame, text="简单快捷指令", variable=self.type_single_var, value="simple")
        self.type_complex_single = Radiobutton(self.type_frame, text="复杂快捷指令", variable=self.type_single_var, value="complex")

        self.name_text = Label(self.name_frame, text="快捷指令名称：")
        self.name_entry = Entry(self.name_frame)

        self.cmd_text = Label(self.cmd_frame, text="快捷指令内容（换行以输入多条指令）：")
        self.cmd_scrolltext = ScrolledText(self.cmd_frame, height=8)

        self.save_button = Button(self.save_frame, text="添加快捷指令")

    def _display(self):
        '''显示控件'''
        self.type_frame.pack(fill=X, padx=10, pady=5)
        self.name_frame.pack(fill=X, padx=(10, 25), pady=5)
        self.cmd_frame.pack(fill=BOTH, padx=10, pady=5)
        self.save_frame.pack(fill=X, padx=10, pady=10)

        self.type_text.pack(side=LEFT, padx=5)
        self.type_simple_single.pack(side=LEFT, padx=5)
        self.type_complex_single.pack(side=LEFT, padx=5)

        self.name_text.pack(side=LEFT, padx=5)
        self.name_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.cmd_text.pack(anchor=NW, padx=5)
        self.cmd_scrolltext.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        self.save_button.pack()

    



class ShortcutCommandsBackend:
    '''快捷指令后端功能实现'''
    def __init__(self):
        pass

if __name__ == "__main__":
    shortcut_cmd_data.reset_table()
    shortcut_cmd_data.add({"cmd_content":"/back", "cmd_name":"列出在线玩家", "cmd_type":"simple"})
    shortcut_cmd_data.add({"cmd_content":"/tpa <player_name>", "cmd_name":"传送至玩家", "cmd_type":"complex"})
    shortcut_cmd_backend = ShortcutCommandsBackend()
    shortcut_cmd_window = ShortcutCommandsGUI(shortcut_cmd_backend)
    mainloop()
