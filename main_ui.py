# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import image_rc
from PyQt5 import QtCore, QtGui, QtWidgets


class Main_Ui_Form(object):
    def setupUi(self, Form):
        Form: QtWidgets.QWidget
        self.clickedItemStr = ''
        Form.setObjectName("Form")
        Form.resize(1304, 955)
        Form.setFixedSize(1304, 955)
        Form.setStyleSheet("")
        self.GroupAndUserFrame = QtWidgets.QFrame(Form)
        self.GroupAndUserFrame.setGeometry(QtCore.QRect(90, 30, 431, 891))
        self.GroupAndUserFrame.setStyleSheet("*{\n"
                                             "font:normal 25px \"微软雅黑\";\n"
                                             "}\n"
                                             "#GroupAndUserFrame{\n"
                                             "/*background:url(:/user/login_background.jpg)*/\n"
                                             "background:rgb(238, 235, 233);\n"
                                             "}\n"
                                             "QLabel\n"
                                             "{\n"
                                             "color:black;\n"
                                             "}\n"
                                             "QLineEdit\n"
                                             "{\n"
                                             "background:transparent;\n"
                                             "border:none;\n"
                                             "color:black;\n"
                                             "border-bottom:1px solid #717072;\n"
                                             "background-color: rgb(255, 255, 255);\n"
                                             "}\n"
                                             "QListWidget\n"
                                             "{\n"
                                             "background:transparent;\n"
                                             "}")
        self.GroupAndUserFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GroupAndUserFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GroupAndUserFrame.setObjectName("GroupAndUserFrame")
        self.toolButton = QtWidgets.QToolButton(self.GroupAndUserFrame)
        self.toolButton.setGeometry(QtCore.QRect(20, 30, 71, 71))
        self.toolButton.setStyleSheet("QToolButton\n"
                                      "{\n"
                                      "background:red;\n"
                                      "border-radius:35px;\n"
                                      "}")
        self.toolButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user/login.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(48, 48))
        self.toolButton.setObjectName("toolButton")
        self.userNameLabel = QtWidgets.QLabel(self.GroupAndUserFrame)
        self.userNameLabel.setGeometry(QtCore.QRect(110, 30, 241, 31))
        self.userNameLabel.setStyleSheet("")
        self.userNameLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.userNameLabel.setText("")
        self.userNameLabel.setObjectName("userNameLabel")
        self.buildGroupLine = QtWidgets.QLineEdit(self.GroupAndUserFrame)
        self.buildGroupLine.setGeometry(QtCore.QRect(160, 80, 261, 31))
        self.buildGroupLine.setStyleSheet("")
        self.buildGroupLine.setInputMask("")
        self.buildGroupLine.setText("")
        self.buildGroupLine.setAlignment(QtCore.Qt.AlignCenter)
        self.buildGroupLine.setObjectName("buildGroupLine")
        self.addGroupLine = QtWidgets.QLineEdit(self.GroupAndUserFrame)
        self.addGroupLine.setGeometry(QtCore.QRect(160, 120, 261, 31))
        self.addGroupLine.setStyleSheet("")
        self.addGroupLine.setInputMask("")
        self.addGroupLine.setText("")
        self.addGroupLine.setAlignment(QtCore.Qt.AlignCenter)
        self.addGroupLine.setObjectName("addGroupLine")
        self.addGroupButton = QtWidgets.QToolButton(self.GroupAndUserFrame)
        self.addGroupButton.setGeometry(QtCore.QRect(110, 120, 41, 31))
        self.addGroupButton.setStyleSheet("QToolButton\n"
                                          "{\n"
                                          "background:transparent;\n"
                                          "}")
        self.addGroupButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/user/buildgroup.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addGroupButton.setIcon(icon1)
        self.addGroupButton.setIconSize(QtCore.QSize(45, 45))
        self.addGroupButton.setObjectName("addGroupButton")
        self.groupListWidget = QtWidgets.QListWidget(self.GroupAndUserFrame)
        self.groupListWidget.setGeometry(QtCore.QRect(10, 260, 411, 631))
        self.groupListWidget.setStyleSheet("")
        self.groupListWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.groupListWidget.setObjectName("groupListWidget")
        self.remindLine = QtWidgets.QLineEdit(self.GroupAndUserFrame)
        self.remindLine.setGeometry(QtCore.QRect(10, 210, 411, 41))
        self.remindLine.setText("")
        self.remindLine.setAlignment(QtCore.Qt.AlignCenter)
        self.remindLine.setReadOnly(True)
        self.remindLine.setObjectName("remindLine")
        self.buildGroupButton = QtWidgets.QToolButton(self.GroupAndUserFrame)
        self.buildGroupButton.setGeometry(QtCore.QRect(100, 80, 51, 31))
        self.buildGroupButton.setStyleSheet("QToolButton\n"
                                            "{\n"
                                            "background:transparent;\n"
                                            "}")
        self.buildGroupButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/user/addgroup.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buildGroupButton.setIcon(icon2)
        self.buildGroupButton.setIconSize(QtCore.QSize(50, 50))
        self.buildGroupButton.setObjectName("buildGroupButton")
        self.userIDLabel = QtWidgets.QLabel(self.GroupAndUserFrame)
        self.userIDLabel.setGeometry(QtCore.QRect(30, 110, 72, 46))
        self.userIDLabel.setText("")
        self.userIDLabel.setObjectName("userIDLabel")
        self.inviteFriendLine = QtWidgets.QLineEdit(self.GroupAndUserFrame)
        self.inviteFriendLine.setGeometry(QtCore.QRect(70, 160, 131, 41))
        self.inviteFriendLine.setStyleSheet("")
        self.inviteFriendLine.setInputMask("")
        self.inviteFriendLine.setText("")
        self.inviteFriendLine.setObjectName("inviteFriendLine")
        self.inviteButton = QtWidgets.QToolButton(self.GroupAndUserFrame)
        self.inviteButton.setGeometry(QtCore.QRect(10, 160, 61, 41))
        self.inviteButton.setStyleSheet("QToolButton\n"
                                        "{\n"
                                        "background:transparent;\n"
                                        "}")
        self.inviteButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/invite.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inviteButton.setIcon(icon3)
        self.inviteButton.setIconSize(QtCore.QSize(45, 45))
        self.inviteButton.setObjectName("inviteButton")
        self.inviteGroupLine = QtWidgets.QLineEdit(self.GroupAndUserFrame)
        self.inviteGroupLine.setGeometry(QtCore.QRect(210, 160, 211, 41))
        self.inviteGroupLine.setStyleSheet("")
        self.inviteGroupLine.setInputMask("")
        self.inviteGroupLine.setText("")
        self.inviteGroupLine.setObjectName("inviteGroupLine")
        self.P2PFrame = QtWidgets.QFrame(Form)
        self.P2PFrame.setGeometry(QtCore.QRect(520, 30, 721, 891))
        self.P2PFrame.setStyleSheet("*{\n"
                                    "font:normal 25px \"微软雅黑\";\n"
                                    "}\n"
                                    "QFrame\n"
                                    "{\n"
                                    "background:white;\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit\n"
                                    "{\n"
                                    "border:none;\n"
                                    "color:black;\n"
                                    "border-bottom:rgb(153, 153, 153);\n"
                                    "background-color:rgb(245, 245, 245);\n"
                                    "border-bottom:1px solid #717072;\n"
                                    "}\n"
                                    "QTextBrowser\n"
                                    "{\n"
                                    "color:black;\n"
                                    "background-color:rgb(245, 245, 245);\n"
                                    "}\n"
                                    "QPushButton\n"
                                    "{\n"
                                    "border:none;\n"
                                    "color:rgb(116, 116, 116);\n"
                                    "background:rgb(229, 229, 229);\n"
                                    "}\n"
                                    "QTextEdit\n"
                                    "{\n"
                                    "border:none;\n"
                                    "}\n"
                                    "QToolButton\n"
                                    "{\n"
                                    "border:none\n"
                                    "}")
        self.P2PFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.P2PFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.P2PFrame.setObjectName("P2PFrame")
        self.sendMessageText = QtWidgets.QTextEdit(self.P2PFrame)
        self.sendMessageText.setGeometry(QtCore.QRect(30, 720, 691, 171))
        self.sendMessageText.setObjectName("sendMessageText")
        self.sendMessageButton = QtWidgets.QPushButton(self.P2PFrame)
        self.sendMessageButton.setGeometry(QtCore.QRect(600, 840, 91, 41))
        self.sendMessageButton.setObjectName("sendMessageButton")

        self.chosenGroupLine = QtWidgets.QLineEdit(self.P2PFrame)
        self.chosenGroupLine.setGeometry(QtCore.QRect(10, 70, 721, 41))
        self.chosenGroupLine.setText("")
        self.chosenGroupLine.setReadOnly(True)
        self.chosenGroupLine.setObjectName("chosenGroupLine")

        self.showTextBrowser = QtWidgets.QTextBrowser(self.P2PFrame)
        self.showTextBrowser.setGeometry(QtCore.QRect(0, 111, 721, 540))
        self.showTextBrowser.setToolTipDuration(-1)
        self.showTextBrowser.setObjectName("showTextBrowser")
        self.p2pCallingRequestLine = QtWidgets.QLineEdit(self.P2PFrame)
        self.p2pCallingRequestLine.setGeometry(QtCore.QRect(0, 0, 611, 71))
        self.p2pCallingRequestLine.setAlignment(QtCore.Qt.AlignCenter)
        self.p2pCallingRequestLine.setReadOnly(False)
        self.p2pCallingRequestLine.setObjectName("p2pCallingRequestLine")
        self.sendFileButton = QtWidgets.QToolButton(self.P2PFrame)
        self.sendFileButton.setGeometry(QtCore.QRect(10, 660, 51, 41))
        self.sendFileButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/user/file.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendFileButton.setIcon(icon4)
        self.sendFileButton.setIconSize(QtCore.QSize(30, 30))
        self.sendFileButton.setObjectName("sendFileButton")
        self.sendAudioButton = QtWidgets.QToolButton(self.P2PFrame)
        self.sendAudioButton.setGeometry(QtCore.QRect(610, 660, 41, 41))
        self.sendAudioButton.setWhatsThis("")
        self.sendAudioButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/user/calling.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendAudioButton.setIcon(icon5)
        self.sendAudioButton.setIconSize(QtCore.QSize(30, 30))
        self.sendAudioButton.setObjectName("sendAudioButton")
        self.sendVideoButton = QtWidgets.QToolButton(self.P2PFrame)
        self.sendVideoButton.setGeometry(QtCore.QRect(660, 660, 41, 41))
        self.sendVideoButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/user/radio.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendVideoButton.setIcon(icon6)
        self.sendVideoButton.setIconSize(QtCore.QSize(30, 30))
        self.sendVideoButton.setObjectName("sendVideoButton")
        self.fileAddressLine = QtWidgets.QLineEdit(self.P2PFrame)
        self.fileAddressLine.setGeometry(QtCore.QRect(60, 660, 401, 41))
        self.fileAddressLine.setStyleSheet("QLineEdit\n"
                                           "{\n"
                                           "background:transparent;\n"
                                           "border:none;\n"
                                           "color:black;\n"
                                           "border-bottom:1px solid #717072;\n"
                                           "background-color: rgb(255, 255, 255);\n"
                                           "}")
        self.fileAddressLine.setInputMask("")
        self.fileAddressLine.setText("")
        self.fileAddressLine.setObjectName("fileAddressLine")
        self.sendOrCloseP2PButton = QtWidgets.QPushButton(self.P2PFrame)
        self.sendOrCloseP2PButton.setGeometry(QtCore.QRect(610, -10, 111, 81))
        self.sendOrCloseP2PButton.setObjectName("sendOrCloseP2PButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.buildGroupLine.setPlaceholderText(_translate("Form", "输入群聊名以创建"))
        self.addGroupLine.setPlaceholderText(_translate("Form", "输入群聊号以加入"))
        self.groupListWidget.setSortingEnabled(False)
        self.remindLine.setPlaceholderText(_translate("Form", "提示消息"))
        self.chosenGroupLine.setPlaceholderText(_translate("Form", "群组名"))
        self.inviteFriendLine.setPlaceholderText(_translate("Form", "输入好友ID"))
        self.inviteGroupLine.setPlaceholderText(
            _translate("Form", "输入群聊ID以邀请"))
        self.sendMessageText.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'微软雅黑\'; font-size:25px; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.sendMessageButton.setText(_translate("Form", "发送"))
        self.p2pCallingRequestLine.setPlaceholderText(
            _translate("Form", "在此处输入好友的ID以快速通话"))
        self.sendAudioButton.setToolTip(_translate("Form", "进行语音通话"))
        self.fileAddressLine.setPlaceholderText(
            _translate("Form", "输入文件地址以传输文件"))
        self.sendOrCloseP2PButton.setText(_translate("Form", "开始"))
