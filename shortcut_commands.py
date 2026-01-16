import os
from tkinter import  *
from tkinter.scrolledtext import ScrolledText
from unittest import enterModuleContext

from databace import shortcut_cmd_data

#代码文件名
FILE_NAME = os.path.basename(__file__)

#后端实例（全局变量）
shortcut_cmd_backend = None

class ShortcutCommandsGUI:
    '''快捷指令管理前端界面实现'''
    def __init__(self, master = None):
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

    def _update_cmd_frame(self):
        '''更新快捷指令框架内容（涉及删除）'''
        for cmd in self.short_cmd_list:
            cmd.undisplay()
        for cmd in self.short_cmd_list:
            cmd.display()

    def delete_cmd(self, cmd):
        '''删除快捷指令'''
        shortcut_cmd_backend.delete_cmd(cmd.id)
        cmd.clear_frame()
        self.short_cmd_list.remove(cmd)
        self._update_cmd_frame()

    def add_cmd(self, cmd_id, cmd_data):
        '''添加快捷指令并更新界面'''
        self.short_cmd_list.append(ShortCmdFrame(cmd_data, cmd_id, self))
        self.short_cmd_list[-1].display()



class ShortCmdFrame:
    '''快捷指令框架类'''
    def __init__(self, cmd_data, cmd_id, master):
        self.cmd_list = cmd_data["cmd_content"].splitlines()
        self.cmd_name = cmd_data["cmd_name"]
        self.cmd_type = cmd_data["cmd_type"]
        self.id = cmd_id
        self.master = master
        self.frame = LabelFrame(master.cmds_frame)
        self._init_widgets()

    def _init_widgets(self):
        '''初始化控件'''
        self.text_frame = Frame(self.frame)
        self.button_frame = Frame(self.frame)

        self.cmd_name_text = Label(self.text_frame, text=f"{"简单" if self.cmd_type == "simple" else "复杂"}快捷指令：{self.cmd_name}")

        self.edit_button = Button(self.button_frame, text="编辑", command=self._on_edit_cmd)
        self.delete_button = Button(self.button_frame, text="删除", command=self._on_delete_cmd)

    def display(self):
        '''显示组件（外部）'''
        self._display()

    def _display(self):
        '''显示组件'''
        self.frame.pack(fill=X, anchor=W, padx=10, pady=5)
        self.text_frame.pack(side=LEFT)
        self.button_frame.pack(side=RIGHT, fill=Y)

        self.cmd_name_text.pack(anchor=W, fill=Y)
            
        self.edit_button.pack(side=RIGHT, fill=Y)
        self.delete_button.pack(side=RIGHT, fill=Y)

    def undisplay(self):
        '''取消隐藏框架（外部）'''
        self.frame.pack_forget()

    def _undisplay_widget(self):
        '''取消隐藏组件（用于编辑刷新）'''
        for frame in (self.text_frame, self.button_frame):
            frame.pack_forget()

    def update(self, new_cmd_data = None):
        '''刷新组件'''
        self._undisplay_widget()
        if new_cmd_data is not None:
            self.cmd_list = new_cmd_data["cmd_content"].splitlines()
            self.cmd_name = new_cmd_data["cmd_name"]
            self.cmd_type = new_cmd_data["cmd_type"]
            self.cmd_name_text.config(text=f"{"简单" if self.cmd_type == "simple" else "复杂"}快捷指令：{self.cmd_name}")
        self._display()

    def clear(self):
        '''清除所有控件'''
        for frame in (self.text_frame, self.button_frame):
            for widget in frame.winfo_children():
                widget.destroy()

    def clear_frame(self):
        '''清除框架'''
        self.frame.destroy()

    def _on_edit_cmd(self):
        '''打开编辑窗口'''
        self.edit_cmd_window = EditCmdWindow(self.master, self, self.id)

    def _on_delete_cmd(self):
        '''删除快捷指令'''
        self.master.delete_cmd(self)
        

class AddCmdWindow:
    '''添加快捷指令窗口'''
    def __init__(self, master):
        self.master = master
        self.WIDTH = 350
        self.HEIGHT = 300

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

        self.save_button = Button(self.save_frame, text="添加快捷指令", command=self._get_input)

        self.warning_text = Label(self.save_frame, fg="red")

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
        self.warning_text.pack(pady=5)

    def _get_input(self):
        '''获取输入内容，校验并保存'''
        cmd_type = self.type_single_var.get()
        cmd_name = self.name_entry.get().strip()
        cmd_content = self.cmd_scrolltext.get("1.0", END).strip()

        #输入校验
        if not self._verification(cmd_name, cmd_content):
            return

        #校验通过
        cmd_data = {
            "cmd_type" : cmd_type,
            "cmd_name" : cmd_name,
            "cmd_content" : cmd_content,
            }

        self._save(cmd_data)
        self.window.destroy()

    def _verification(self, cmd_name, cmd_content) -> bool:
        '''输入内容校验，显示校验失败原因'''
        result = True
        if cmd_name == "":          #空校验
            self.warning_text.config(text="快捷指令名称不能为空！")
            result = False
        elif cmd_content == "":
            self.warning_text.config(text="快捷指令内容不能为空！")
            result = False
        
        for cmd in self.master.short_cmd_list:  #重复校验
            if cmd_name == cmd.cmd_name:
                self.warning_text.config(text="快捷指令名称不能重复！")
                result = False

        return result

    def _save(self, cmd_data):
        '''保存账户（添加）'''
        cmd_id = shortcut_cmd_backend.add_cmd(cmd_data)
        self.master.add_cmd(cmd_id, cmd_data)


class EditCmdWindow(AddCmdWindow):
    '''编辑快捷指令窗口'''
    def __init__(self, master, submaster, cmd_id):
        cmd_data = shortcut_cmd_backend.get_cmd_data(cmd_id)
        self.id = cmd_id
        self.submaster = submaster
        self.cmd_type = cmd_data["cmd_type"]
        self.cmd_content = cmd_data["cmd_content"]
        self.cmd_name = cmd_data["cmd_name"]
        super().__init__(master)

    def _init_window(self):
        super()._init_window()
        self.window.title("编辑快捷指令")

    def _init_widgets(self):
        super()._init_widgets()
        self.type_single_var.set(self.cmd_type)
        self.save_button.config(text="保存快捷指令")

        self.name_entry.insert(0, self.cmd_name)
        self.cmd_scrolltext.insert("1.0", self.cmd_content)

    def _display(self):
        super()._display()
        self.type_simple_single.pack_forget()
        self.type_complex_single.pack_forget()
        if self.cmd_type == "simple":
            self.type_simple_single.pack(side=LEFT, padx=5)
        elif self.cmd_type == "complex":
            self.type_complex_single.pack(side=LEFT, padx=5)

    def _save(self, cmd_data):
        '''保存快捷指令（编辑）'''
        shortcut_cmd_backend.edit_cmd(self.id, cmd_data)
        self.submaster.update(cmd_data)

    def _verification(self, cmd_name, cmd_content) -> bool:
        '''输入内容校验，显示校验失败原因（重写）'''
        result = True
        if cmd_name == "":          #空校验
            self.warning_text.config(text="快捷指令名称不能为空！")
            result = False
        elif cmd_content == "":
            self.warning_text.config(text="快捷指令内容不能为空！")
            result = False
        
        for cmd in self.master.short_cmd_list:  #重复校验（不包括自己）
            if cmd_name == cmd.cmd_name and self.submaster != cmd:
                self.warning_text.config(text="快捷指令名称不能重复！")
                result = False

        return result




class ShortcutCommandsBackend:
    '''快捷指令后端功能实现'''
    _instance = None
    _initialized = False

    def __new__(cls):
        '''单例类'''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return

        self.__class__._initialized = True

    def add_cmd(self, cmd_data) -> int:
        '''新增快捷指令（返回cmd_id）'''
        cmd_id = shortcut_cmd_data.add(cmd_data)
        return cmd_id

    def delete_cmd(self, cmd_id):
        '''删除快捷指令'''
        shortcut_cmd_data.delete(cmd_id)

    def edit_cmd(self, cmd_id, cmd_data):
        '''修改快捷指令内容'''
        shortcut_cmd_data.update(cmd_id, cmd_data)

    def get_cmd_data(self, cmd_id):
        '''获取快捷指令信息'''
        return shortcut_cmd_data.selete_all(cmd_id)


if __name__ == "__main__":
    #shortcut_cmd_data.reset_table()
    #shortcut_cmd_data.add({"cmd_content":"/back", "cmd_name":"列出在线玩家", "cmd_type":"simple"})
    #shortcut_cmd_data.add({"cmd_content":"/tpa <player_name>", "cmd_name":"传送至玩家", "cmd_type":"complex"})
    shortcut_cmd_backend = ShortcutCommandsBackend()
    shortcut_cmd_window = ShortcutCommandsGUI(shortcut_cmd_backend)
    mainloop()



else:
    shortcut_cmd_backend = ShortcutCommandsBackend()
    shortcut_cmd_window = ShortcutCommandsGUI(shortcut_cmd_backend)

