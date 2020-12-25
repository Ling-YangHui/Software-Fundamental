import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from login_ui import *
from clientCore import *
from main import *
import socket


class Login(QtWidgets.QWidget, Ui_Form):
    # 初始化
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.Register_Line.clicked.connect(self.sendRegisterRequest)
        self.Login_Button.clicked.connect(self.sendLoginRequest)
        self.clientCore = CLIENTCORE()
        self.ipAddr = self.clientCore.localIP

    # 发送注册信息，QLineEdit类中text()方法返回框中输入的文本
    def sendRegisterRequest(self):
        if self.Password_Line.text().__len__() < 6:
            self.Dispaly_Lable.setText('密码强度不足')
            return
        if self.clientCore.register(self.Username_Line.text(), self.Password_Line.text()):
            while self.clientCore.registerID == '':
                continue
            self.Dispaly_Lable.setText(
                "注册成功！" + "ID为: " + self.clientCore.registerID)
        else:
            self.Dispaly_Lable.setText("注册失败，请重试")

    def sendLoginRequest(self):
        try:
            userName = self.Username_Line.text()
            if userName.isdigit() == False:
                self.Dispaly_Lable.setText("用户名或密码错误")
                return
            if self.clientCore.login(self.Username_Line.text(), self.Password_Line.text(), self.ipAddr):
                global main
                main = Main(self.clientCore)
                main.show()
                self.close()
                # 下面打开主界面，打开主界面以后要把self.clientCore传值过去，客户端核心不能被重载
            else:
                self.Dispaly_Lable.setText("账号或密码错误")
        except clientError:
            self.Dispaly_Lable.setText("账号或密码错误")
