# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_server.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 480)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget_main = QTabWidget(Dialog)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tab_logged_servers = QWidget()
        self.tab_logged_servers.setObjectName(u"tab_logged_servers")
        self.verticalLayout = QVBoxLayout(self.tab_logged_servers)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_search_servers = QLineEdit(self.tab_logged_servers)
        self.lineEdit_search_servers.setObjectName(u"lineEdit_search_servers")

        self.horizontalLayout_2.addWidget(self.lineEdit_search_servers)

        self.pushButton_search_servers = QPushButton(self.tab_logged_servers)
        self.pushButton_search_servers.setObjectName(u"pushButton_search_servers")

        self.horizontalLayout_2.addWidget(self.pushButton_search_servers)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listWidget_servers = QListWidget(self.tab_logged_servers)
        icon = QIcon()
        icon.addFile(u"C:/Users/12110/Pictures/0b9a9e29a1faf3aa91fef2ac0c78ae220d29c7e9.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        __qlistwidgetitem = QListWidgetItem(self.listWidget_servers)
        __qlistwidgetitem.setIcon(icon);
        QListWidgetItem(self.listWidget_servers)
        QListWidgetItem(self.listWidget_servers)
        QListWidgetItem(self.listWidget_servers)
        QListWidgetItem(self.listWidget_servers)
        QListWidgetItem(self.listWidget_servers)
        self.listWidget_servers.setObjectName(u"listWidget_servers")

        self.verticalLayout.addWidget(self.listWidget_servers)

        self.tabWidget_main.addTab(self.tab_logged_servers, "")
        self.tab_custom_server = QWidget()
        self.tab_custom_server.setObjectName(u"tab_custom_server")
        self.verticalLayout_2 = QVBoxLayout(self.tab_custom_server)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_server_name = QLabel(self.tab_custom_server)
        self.label_server_name.setObjectName(u"label_server_name")

        self.horizontalLayout_3.addWidget(self.label_server_name)

        self.lineEdit_server_name = QLineEdit(self.tab_custom_server)
        self.lineEdit_server_name.setObjectName(u"lineEdit_server_name")

        self.horizontalLayout_3.addWidget(self.lineEdit_server_name)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget = QWidget(self.tab_custom_server)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout_7 = QHBoxLayout(self.widget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_server_ip = QLabel(self.widget)
        self.label_server_ip.setObjectName(u"label_server_ip")

        self.horizontalLayout_7.addWidget(self.label_server_ip)

        self.lineEdit_server_ip = QLineEdit(self.widget)
        self.lineEdit_server_ip.setObjectName(u"lineEdit_server_ip")
        self.lineEdit_server_ip.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_7.addWidget(self.lineEdit_server_ip)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.lineEdit_server_port = QLineEdit(self.widget)
        self.lineEdit_server_port.setObjectName(u"lineEdit_server_port")
        self.lineEdit_server_port.setMinimumSize(QSize(60, 0))
        self.lineEdit_server_port.setMaximumSize(QSize(60, 16777215))
        self.lineEdit_server_port.setMaxLength(5)

        self.horizontalLayout_7.addWidget(self.lineEdit_server_port)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addWidget(self.widget)

        self.widget_standy_ip_list = QWidget(self.tab_custom_server)
        self.widget_standy_ip_list.setObjectName(u"widget_standy_ip_list")

        self.verticalLayout_3.addWidget(self.widget_standy_ip_list)

        self.pushButton_add_standby_ip = QPushButton(self.tab_custom_server)
        self.pushButton_add_standby_ip.setObjectName(u"pushButton_add_standby_ip")
        self.pushButton_add_standby_ip.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_3.addWidget(self.pushButton_add_standby_ip)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_add_server = QPushButton(self.tab_custom_server)
        self.pushButton_add_server.setObjectName(u"pushButton_add_server")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_add_server.sizePolicy().hasHeightForWidth())
        self.pushButton_add_server.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.pushButton_add_server)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget_main.addTab(self.tab_custom_server, "")

        self.horizontalLayout.addWidget(self.tabWidget_main)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lineEdit_search_servers.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8f93\u5165\u670d\u52a1\u5668\u540d\u6216IP\u5730\u5740\u4ee5\u641c\u7d22", None))
        self.pushButton_search_servers.setText(QCoreApplication.translate("Dialog", u"\u641c\u7d22", None))

        __sortingEnabled = self.listWidget_servers.isSortingEnabled()
        self.listWidget_servers.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget_servers.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Dialog", u"\u8292\u679c\u65b9\u5757\u7c89\u4e1d\u670d\n"
"je.server.mangocraft.net", None));
        ___qlistwidgetitem1 = self.listWidget_servers.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Dialog", u"\u6d4b\u8bd5\u670d\u52a1\u56681", None));
        ___qlistwidgetitem2 = self.listWidget_servers.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Dialog", u"\u6d4b\u8bd5\u670d\u52a1\u56682", None));
        ___qlistwidgetitem3 = self.listWidget_servers.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Dialog", u"\u6d4b\u8bd5\u670d\u52a1\u5668c", None));
        ___qlistwidgetitem4 = self.listWidget_servers.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Dialog", u"\u6d4b\u8bd5\u670d\u52a1\u5668D", None));
        ___qlistwidgetitem5 = self.listWidget_servers.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Dialog", u"ceshigiaogiaogiao!", None));
        self.listWidget_servers.setSortingEnabled(__sortingEnabled)

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_logged_servers), QCoreApplication.translate("Dialog", u"\u5df2\u6536\u5f55\u670d\u52a1\u5668", None))
        self.label_server_name.setText(QCoreApplication.translate("Dialog", u"       \u670d\u52a1\u5668\u540d\u79f0\uff1a", None))
        self.label_server_ip.setText(QCoreApplication.translate("Dialog", u"    IP\u5730\u5740\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u7aef\u53e3\uff1a", None))
        self.lineEdit_server_port.setInputMask("")
        self.pushButton_add_standby_ip.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0\u5907\u7528\u5730\u5740", None))
        self.pushButton_add_server.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0\u670d\u52a1\u5668", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_custom_server), QCoreApplication.translate("Dialog", u"\u81ea\u5b9a\u4e49\u670d\u52a1\u5668", None))
    # retranslateUi

