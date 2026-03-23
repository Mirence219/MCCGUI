# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'standby_server.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_Form_standby_server(object):
    def setupUi(self, Form_standby_server):
        if not Form_standby_server.objectName():
            Form_standby_server.setObjectName(u"Form_standby_server")
        Form_standby_server.resize(667, 124)
        self.horizontalLayout = QHBoxLayout(Form_standby_server)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_standby_server_ip = QLabel(Form_standby_server)
        self.label_standby_server_ip.setObjectName(u"label_standby_server_ip")

        self.horizontalLayout.addWidget(self.label_standby_server_ip)

        self.lineEdit_standby_server_ip = QLineEdit(Form_standby_server)
        self.lineEdit_standby_server_ip.setObjectName(u"lineEdit_standby_server_ip")
        self.lineEdit_standby_server_ip.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.lineEdit_standby_server_ip)

        self.label_standby_server_port = QLabel(Form_standby_server)
        self.label_standby_server_port.setObjectName(u"label_standby_server_port")

        self.horizontalLayout.addWidget(self.label_standby_server_port)

        self.lineEdit_standby_server_port = QLineEdit(Form_standby_server)
        self.lineEdit_standby_server_port.setObjectName(u"lineEdit_standby_server_port")
        self.lineEdit_standby_server_port.setMinimumSize(QSize(60, 0))
        self.lineEdit_standby_server_port.setMaximumSize(QSize(60, 16777215))
        self.lineEdit_standby_server_port.setMaxLength(5)

        self.horizontalLayout.addWidget(self.lineEdit_standby_server_port)

        self.pushButton_remove_standy_server = QPushButton(Form_standby_server)
        self.pushButton_remove_standy_server.setObjectName(u"pushButton_remove_standy_server")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_remove_standy_server.sizePolicy().hasHeightForWidth())
        self.pushButton_remove_standy_server.setSizePolicy(sizePolicy)
        self.pushButton_remove_standy_server.setMaximumSize(QSize(27, 16777215))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        self.pushButton_remove_standy_server.setIcon(icon)
        self.pushButton_remove_standy_server.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.pushButton_remove_standy_server)

        self.horizontalSpacer_3 = QSpacerItem(68, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.retranslateUi(Form_standby_server)

        QMetaObject.connectSlotsByName(Form_standby_server)
    # setupUi

    def retranslateUi(self, Form_standby_server):
        Form_standby_server.setWindowTitle(QCoreApplication.translate("Form_standby_server", u"Form", None))
        self.label_standby_server_ip.setText(QCoreApplication.translate("Form_standby_server", u"    \u5907\u7528\u5730\u57401\uff1a", None))
        self.label_standby_server_port.setText(QCoreApplication.translate("Form_standby_server", u"\u7aef\u53e3\uff1a", None))
        self.lineEdit_standby_server_port.setInputMask("")
#if QT_CONFIG(tooltip)
        self.pushButton_remove_standy_server.setToolTip(QCoreApplication.translate("Form_standby_server", u"\u5220\u9664\u6b64\u884c", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_remove_standy_server.setText("")
    # retranslateUi

