# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(544, 398)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget_main = QTabWidget(self.centralwidget)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setTabPosition(QTabWidget.TabPosition.West)
        self.tab_home = QWidget()
        self.tab_home.setObjectName(u"tab_home")
        self.gridLayout = QGridLayout(self.tab_home)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget_home = QTabWidget(self.tab_home)
        self.tabWidget_home.setObjectName(u"tabWidget_home")
        self.tabWidget_home.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_home.setMovable(False)
        self.tab_mangocraft = QWidget()
        self.tab_mangocraft.setObjectName(u"tab_mangocraft")
        self.gridLayout_2 = QGridLayout(self.tab_mangocraft)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(self.tab_mangocraft)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 304))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_add_instance = QFrame(self.scrollAreaWidgetContents)
        self.frame_add_instance.setObjectName(u"frame_add_instance")
        self.frame_add_instance.setMinimumSize(QSize(150, 150))
        self.frame_add_instance.setMaximumSize(QSize(150, 150))
        self.frame_add_instance.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.frame_add_instance.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_add_instance.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_add_instance)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.frame_add_instance)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)


        self.gridLayout_3.addWidget(self.frame_add_instance, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget_home.addTab(self.tab_mangocraft, "")
        self.tab_add_server = QWidget()
        self.tab_add_server.setObjectName(u"tab_add_server")
        self.gridLayout_4 = QGridLayout(self.tab_add_server)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_add_server = QPushButton(self.tab_add_server)
        self.pushButton_add_server.setObjectName(u"pushButton_add_server")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add_server.sizePolicy().hasHeightForWidth())
        self.pushButton_add_server.setSizePolicy(sizePolicy)
        self.pushButton_add_server.setMaximumSize(QSize(150, 150))
        self.pushButton_add_server.setAutoExclusive(False)
        self.pushButton_add_server.setAutoDefault(True)
        self.pushButton_add_server.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_add_server, 0, 0, 1, 1)

        self.tabWidget_home.addTab(self.tab_add_server, "")

        self.gridLayout.addWidget(self.tabWidget_home, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_home, "")
        self.tab_custom = QWidget()
        self.tab_custom.setObjectName(u"tab_custom")
        self.tabWidget_main.addTab(self.tab_custom, "")
        self.tab_setting = QWidget()
        self.tab_setting.setObjectName(u"tab_setting")
        self.tabWidget_main.addTab(self.tab_setting, "")

        self.verticalLayout_2.addWidget(self.tabWidget_main)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_home.setCurrentIndex(0)
        self.pushButton_add_server.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u5b9e\u4f8b", None))
        self.tabWidget_home.setTabText(self.tabWidget_home.indexOf(self.tab_mangocraft), QCoreApplication.translate("MainWindow", u"\u8292\u679c\u65b9\u5757", None))
        self.pushButton_add_server.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u670d\u52a1\u5668", None))
        self.tabWidget_home.setTabText(self.tabWidget_home.indexOf(self.tab_add_server), QCoreApplication.translate("MainWindow", u"+", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_home), QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_custom), QCoreApplication.translate("MainWindow", u"\u4e2a\u6027\u5316", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setting), QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
    # retranslateUi

