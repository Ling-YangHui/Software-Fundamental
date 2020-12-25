# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import user_rc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(936, 660)
        Form.setFixedSize(936, 660)
        Form.setStyleSheet("*\n"
                           "{\n"
                           "font:normal 25px \"微软雅黑\";\n"
                           "}\n"


                           "QLabel\n"
                           "{\n"
                           "color:white;\n"
                           "text-align: center\n"
                           "}\n"

                           "QFrame\n"
                           "{\n"
                           "background:#333\n"
                           "}\n"

                           "QToolButton\n"
                           "{\n"
                           "background:red;\n"
                           "border-radius:45px;\n"
                           "}\n"

                           "QPushButton\n"
                           "{\n"
                           "color:white;\n"
                           "background:red;\n"
                           "border-radius:15px;\n"
                           "}\n"

                           "QPushButton:hover\n"
                           "{\n"
                           "background:blue;\n"
                           "}\n"

                           "QLineEdit{\n"
                           "background:transparent;\n"
                           "border:none;\n"
                           "color:white;\n"
                           "border-bottom:1px solid #717072;\n"
                           "}")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(
            QPixmap(os.getcwd()+'/ClientSource/Image/login_background.jpg')))
        Form.setPalette(palette)

        self.Login_Window = QtWidgets.QFrame(Form)
        self.Login_Window.setGeometry(QtCore.QRect(290, 160, 361, 351))
        self.Login_Window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Login_Window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Login_Window.setObjectName("Login_Window")
        self.Dispaly_Lable = QtWidgets.QLabel(self.Login_Window)
        self.Dispaly_Lable.setGeometry(QtCore.QRect(30, 50, 251, 41))
        self.Dispaly_Lable.setObjectName("Dispaly_Lable")
        self.Login_Button = QtWidgets.QPushButton(self.Login_Window)
        self.Login_Button.setGeometry(QtCore.QRect(190, 290, 151, 41))
        self.Login_Button.setObjectName("Login_Button")
        self.Register_Line = QtWidgets.QPushButton(self.Login_Window)
        self.Register_Line.setGeometry(QtCore.QRect(20, 290, 151, 41))
        self.Register_Line.setObjectName("Register_Line")
        self.Username_Line = QtWidgets.QLineEdit(self.Login_Window)
        self.Username_Line.setGeometry(QtCore.QRect(50, 130, 261, 41))
        self.Username_Line.setInputMask("")
        self.Username_Line.setText("")
        self.Username_Line.setObjectName("Username_Line")
        self.Password_Line = QtWidgets.QLineEdit(self.Login_Window)
        self.Password_Line.setGeometry(QtCore.QRect(50, 200, 261, 41))
        self.Password_Line.setInputMask("")
        self.Password_Line.setText("")
        self.Password_Line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_Line.setObjectName("Password_Line")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(430, 110, 91, 91))
        self.toolButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user/login.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(64, 64))
        self.toolButton.setObjectName("toolButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "登录"))
        self.Dispaly_Lable.setText(_translate("Form", "注册/登录"))
        self.Login_Button.setText(_translate("Form", "登录"))
        self.Register_Line.setText(_translate("Form", "注册"))
        self.Username_Line.setPlaceholderText(_translate("Form", "注册用户名/登录ID"))
        self.Password_Line.setPlaceholderText(_translate("Form", "密码"))
