from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QSortFilterProxyModel, Qt

from src.ui.add_server.ui_add_server import Ui_Dialog_add_server
from src.ui.add_server.ui_standby_server import Ui_Form_standby_server

class AddServerDialog(QDialog, Ui_Dialog_add_server):
    '''添加服务器窗口类'''
    def __init__(self, master):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("添加服务器")
     
        self._init_tab_logged_server()
        self._init_tab_custom_server()
        
        
    def _init_tab_logged_server(self):
        '''添加已收录服务器初始化'''
        self.pushButton_search_servers.clicked.connect(self.on_pushButton_search_servers_clicked)


    def _init_tab_custom_server(self):
        '''添加自定义服务器页初始化'''
        self.standby_ip_widgets_dic = {}    #备用ip输入行列表

        self.pushButton_add_standby_ip.clicked.connect(self.on_pushButton_add_standby_ip_clicked)     
        #self.pushButton_add_server.clicked.connect(self.on_pushButton_add_server_clicked)


    def on_pushButton_add_standby_ip_clicked(self):
        '''添加备用IP输入行'''
        print("[DEBUG]点击“添加备用地址”")
        new_widgets = QWidget(self.widget_standy_ip_list)
        new_widgets_ui = Ui_Form_standby_server()
        new_widgets_ui.setupUi(new_widgets)
        new_widgets_ui.label_standby_server_ip.setText(f"备用地址{len(self.standby_ip_widgets_dic) + 1}：")   #设置备用IP序号
        new_widgets_ui.pushButton_remove_standy_server.clicked.connect(lambda _: self.on_pushButton_remove_standy_server_clicked(new_widgets))  #为删除按钮设置槽
        layout = self.widget_standy_ip_list.layout() or QVBoxLayout(self.widget_standy_ip_list)
        layout.addWidget(new_widgets)
        self.standby_ip_widgets_dic.update({new_widgets: new_widgets_ui})


    def on_pushButton_remove_standy_server_clicked(self, standby_server_widgets):
        '''删除备用IP输入行'''
        print("[DEBUG]点击“删除备用行”")
        self.standby_ip_widgets_dic.pop(standby_server_widgets)
        standby_server_widgets.deleteLater()
        index = 0
        for widgets, ui in self.standby_ip_widgets_dic.items():
            index += 1
            ui.label_standby_server_ip.setText(f"备用地址{index}：")


    def on_pushButton_add_server_clicked(self):
        '''添加服务器'''
        print("[DEBUG]点击“添加服务器”")


    def on_pushButton_search_servers_clicked(self):
        '''搜索服务器'''
        print("[DEBUG]点击“搜索”")
        keyword = self.lineEdit_search_servers.text().strip()
        for index in range(self.listWidget_servers.count()):
            item = self.listWidget_servers.item(index)
            if keyword == "" or keyword.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
        print(f"[DEBUG]已筛选“{keyword}”")












