from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from src.ui.add_server.ui_add_server import Ui_Dialog
from src.ui.add_server.ui_standby_server import Ui_Form_standby_server

class AddServerDialog(QDialog, Ui_Dialog):
    '''添加服务器窗口类'''
    def __init__(self, master):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("添加服务器")

        self.standby_ip_widgets = []    #备用ip输入行列表

        self.pushButton_add_standby_ip.clicked.connect(self.on_pushButton_add_standby_ip_clicked)
        self.pushButton_add_server.clicked.connect(self.on_pushButton_add_server_clicked)
        

    def on_pushButton_add_standby_ip_clicked(self):
        '''添加备用IP输入行'''
        print("[DEBUG]点击“添加备用地址”")
        new_widget = QWidget(self.widget_standy_ip_list)
        new_widget_ui = Ui_Form_standby_server()
        new_widget_ui.setupUi(new_widget)
        new_widget_ui.label_standby_server_ip.setText(f"备用IP{len(self.standby_ip_widgets) + 1}")   #设置备用IP序号
        new_widget_ui.pushButton_remove_standy_server.clicked.connect(self.on_pushButton_remove_standy_server_clicked)
        layout = self.widget_standy_ip_list.layout() or QVBoxLayout(self.widget_standy_ip_list)
        layout.addWidget(new_widget)
        self.standby_ip_widgets.append((new_widget, new_widget_ui))

    def on_pushButton_remove_standy_server_clicked(self):
        '''删除备用IP行'''
        print("[DEBUG]点击“删除备用行”")


    def on_pushButton_add_server_clicked(self):
        '''添加服务器'''
        print("[DEBUG]点击“添加服务器”")











