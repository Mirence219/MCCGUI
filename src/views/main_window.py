from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys

from __version__ import __version__
from src.ui.main.ui_main import Ui_MainWindow
from src.views.add_server_window import AddServerDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    '''主窗口类'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"MCCGUI v{__version__}")
        self.pushButton_add_server.clicked.connect(self.on_pushButton_add_server_clicked)

    def on_pushButton_add_server_clicked(self):
        '''打开添加服务器窗口'''
        print("[DEBUG]点击“添加服务器”按钮")
        self.add_server_window = AddServerDialog(self)
        self.add_server_window.setModal(True)
        self.add_server_window.exec()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


