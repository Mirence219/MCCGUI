# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_instance.ui'
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
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(616, 419)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_2 = QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget = QWidget(self.tab)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.radioButton = QRadioButton(self.widget_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)
        self.radioButton.setAutoRepeat(False)

        self.horizontalLayout_6.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.widget_2)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setAutoRepeat(False)

        self.horizontalLayout_6.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.widget_2)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_6.addWidget(self.radioButton_3)


        self.horizontalLayout_5.addWidget(self.widget_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout.addWidget(self.widget_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setLocale(QLocale(QLocale.Chinese, QLocale.China))

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addWidget(self.widget)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u8d26\u6237\u7c7b\u578b\uff1a", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"\u7b2c\u4e09\u65b9\u8d26\u6237", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"\u6b63\u7248\u8d26\u6237", None))
        self.radioButton_3.setText(QCoreApplication.translate("Dialog", u"\u79bb\u7ebf\u8d26\u6237", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u521b\u5efa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"\u8d26\u6237\u914d\u7f6e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"\u5ba2\u6237\u7aef\u914d\u7f6e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
    # retranslateUi

