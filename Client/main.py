import sys
import datetime
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import QtCore
from clientCore import CLIENTCORE
from main_ui import *
from PyQt5.Qt import QMessageBox
# from groupchat import *


class Main(QtWidgets.QWidget, Main_Ui_Form):
    # 初始化
    messageSignal = QtCore.pyqtSignal(str)  # 消息信号槽
    groupRefreshSignal = QtCore.pyqtSignal(str)  # 群组信号槽
    askCallingSignal = QtCore.pyqtSignal(str)  # 电话请求信号槽
    showCallingSignal = QtCore.pyqtSignal(str)  # 电话接通信号槽

    def __init__(self, client, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.groupChatWidgetList = []
        self.clientCore: CLIENTCORE
        self.clientCore = client
        self.buildGroupButton.clicked.connect(self.buildGroupRequest)
        self.addGroupButton.clicked.connect(self.addGroupRequest)
        self.inviteButton.clicked.connect(self.inviteAddGroup)
        self.sendOrCloseP2PButton.clicked.connect(self.sendP2PCallingRequset)
        self.sendMessageButton.clicked.connect(self.sendP2PMessage)

        # self.sendVideoButton.clicked.connect(self.sendP2PAudioRequest)
        # self.sendAudioButton.clicked.connect(self.sendP2PVideoRequest)
        # self.sendFileButton.clicked.connect(self.sendP2PFileRequest)
        self.groupListStr = []
        self.groupMessage = []
        # 标志
        self.finishedGroupInit = False
        self.nowChosenGroup = 0
        self.isCalling = False

        self.getMessageThread = threading.Thread(
            target=self.getMessageFromCore)
        self.getMessageThread.setDaemon(True)
        self.getMessageThread.start()

        # 线程信号槽分布
        self.messageSignal.connect(self.showMessage)
        self.groupRefreshSignal.connect(self.groupListWidgetCmd)
        self.askCallingSignal.connect(self.beAskedCalling)
        self.showCallingSignal.connect(self.showCalling)

        self.groupListWidget.doubleClicked.connect(self.changeGroup)
        # self.groupListWidget.clicked.connect(self.changeGroup)
        self.clientCore.refreshGroupList()
        self.userNameLabel.setText(self.clientCore.userName)
        self.userIDLabel.setText(self.clientCore.ID)

    # 创建群聊窗口实体
    # def createGroupList(self):
    #     for group in self.clientCore.groupList:
    #         newGroupChatWidget = GroupChat(self.clientCore,group.groupName,group.groupID)
    #         self.groupChatWidgetList.append(newGroupChatWidget)

    def getMessageFromCore(self):
        while True:
            self.clientCore.sendToFrontEvent.wait()
            try:
                while not self.clientCore.sendToFrontQueue.empty():
                    string: str
                    string = self.clientCore.sendToFrontQueue.get()
                    if string.find('GroupMessage') != -1:
                        messageList = string.split('$', 5)
                        group = str(messageList[2]) + \
                            ' (' + str(messageList[1]) + ')'
                        index = self.groupListStr.index(group)
                        if index == self.nowChosenGroup:
                            self.messageSignal.emit("{}  {} :\n{}".format(
                                messageList[3],  datetime.datetime.now().strftime('%F-%T'), messageList[4]))
                        self.groupMessage[index].append("{}  {} :\n{}".format(
                            messageList[3], datetime.datetime.now().strftime('%F-%T'), messageList[4]))

                    if string == 'UserGroupListRefresh':
                        for index in self.clientCore.groupList:
                            group = str(index[1]) + ' (' + str(index[0]) + ')'
                            if not (group in self.groupListStr):
                                self.groupListStr.append(group)
                                self.groupMessage.append([])
                        self.finishedGroupInit = True
                        self.groupRefreshSignal.emit('trig')

                    if string == 'AskingCalling':
                        self.askCallingSignal.emit('trig')

                    if string == 'ReceiveCalling':
                        self.showCallingSignal.emit('open')

                    if string == 'CallingEnd':
                        self.showCallingSignal.emit('close')

                self.clientCore.sendToFrontEvent.clear()
            except Exception:
                continue

    def showCalling(self, string):
        if string == 'open':
            self.p2pCallingRequestLine.setText(
                self.clientCore.requireCallingTarget + ' 通话中')
            self.isCalling = True
            self.sendOrCloseP2PButton.setText('关闭')
            self.p2pCallingRequestLine.setReadOnly(False)
        elif string == 'close':
            self.p2pCallingRequestLine.clear()
            self.isCalling = False
            self.sendOrCloseP2PButton.setText('开始')
            self.p2pCallingRequestLine.setReadOnly(False)

    def beAskedCalling(self, string):
        askCallingBox = QMessageBox(
            QMessageBox.Critical, '通信请求', self.clientCore.requireCallingTarget + ' 请求通话', QMessageBox.NoButton, self)
        acceptButton = askCallingBox.addButton('接受', QMessageBox.YesRole)
        refuseButton = askCallingBox.addButton('拒绝', QMessageBox.YesRole)
        askCallingBox.setIcon(1)
        askCallingBox.setGeometry(900, 500, 0, 0)
        acceptButton.clicked.connect(self.clientCore.receiveCalling)
        acceptButton.clicked.connect(askCallingBox.close)
        refuseButton.clicked.connect(self.clientCore.refuseCalling)
        refuseButton.clicked.connect(askCallingBox.close)
        askCallingBox.show()

    def buildGroupRequest(self):
        if self.buildGroupLine.text() != '':
            try:
                if not self.clientCore.buildGroup(self.buildGroupLine.text()):
                    self.remindLine.setText("建群失败，请重试！")
                else:
                    self.remindLine.setText('建群成功')
                self.buildGroupLine.clear()
            except Exception:
                self.remindLine.setText("建群失败，请重试！")

    def addGroupRequest(self):
        if self.addGroupLine.text() != '':
            try:
                if self.addGroupLine.text().isdigit() == False:
                    self.remindLine.setText("加群失败，请检查群组ID后重试！")
                    return
                if not self.clientCore.addGroup(self.userIDLabel.text(), self.addGroupLine.text()):
                    self.remindLine.setText("加群失败，请检查群组ID后重试！")
                else:
                    self.remindLine.setText('加群成功')
                self.addGroupLine.clear()
            except Exception:
                self.remindLine.setText("加群失败，请检查群组ID后重试！")

    def inviteAddGroup(self):
        if self.inviteFriendLine.text() != '':
            try:
                friendID: str = self.inviteFriendLine.text()
                groupID: str = self.inviteGroupLine.text()
                if groupID == '':
                    groupID = self.clientCore.groupList[self.nowChosenGroup][0]
                if friendID.isdigit() == False or groupID.isdigit() == False:
                    self.remindLine.setText("邀请失败，请检查好友及群组ID后重试！")
                    return
                if not self.clientCore.addGroup(friendID, groupID):
                    self.remindLine.setText("邀请失败，请检查好友及群组ID后重试！")
                else:
                    self.remindLine.setText("邀请成功！")
                self.inviteGroupLine.clear()
                self.inviteFriendLine.clear()
            except Exception:
                self.remindLine.setText("邀请失败，请检查好友及群组ID后重试！")

    def sendP2PCallingRequset(self):
        print(1)
        if self.p2pCallingRequestLine.text() != '' and self.p2pCallingRequestLine.text().isdigit() and self.isCalling == False:
            if self.clientCore.requireCalling(self.p2pCallingRequestLine.text()):
                self.p2pCallingRequestLine.setText(
                    "{} 通话中".format(self.p2pCallingRequestLine.text()))
                self.p2pCallingRequestLine.setReadOnly(True)
                self.sendOrCloseP2PButton.setText("关闭")
                self.isCalling = True
        elif self.isCalling == True:
            if self.clientCore.closeCalling():
                self.p2pCallingRequestLine.clear()
                self.p2pCallingRequestLine.setReadOnly(False)
                self.sendOrCloseP2PButton.setText("开始")
                self.isCalling = False

    def sendP2PMessage(self):
        # toPlainText()方法可以获取当前文本编辑器内的多行文本
        if self.sendMessageText.toPlainText() != '':
            # //此处添加发送信息代码
            if True:
                self.clientCore.sendMessage(self.sendMessageText.toPlainText(
                ), self.clientCore.groupList[self.nowChosenGroup][0])
                self.sendMessageText.clear()

    def showP2PMessage(self, Name, ID, message):
        self.showTextBrowser.append("{}({})  {} :\n{}".format(
            Name, ID, datetime.datetime.now().strftime('%F-%T'), message))

    # 槽函数
    def groupListWidgetCmd(self, groupList):
        self.groupListWidget.clear()
        self.groupListWidget.addItems(self.groupListStr)

    def showMessage(self, message):
        self.showTextBrowser.append(message)

    def changeGroup(self):
        chosenGroup = self.groupListWidget.selectedIndexes()[0].row()
        self.chosenGroupLine.setText(self.groupListStr[chosenGroup])
        if self.nowChosenGroup == chosenGroup:
            return
        self.nowChosenGroup = chosenGroup
        self.chosenGroupLine.setText(self.groupListStr[self.nowChosenGroup])
        self.showTextBrowser.clear()
        for i in self.groupMessage[self.nowChosenGroup]:
            self.showMessage(i)

    # def sendP2PAudioRequest(self):

    # def sendP2PVideoRequest(self):

    # def sendP2PFileRequest(self):
    #     if self.fileAddressLine != '':
    #         if True:


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     Client = clientCore()
#     Client.userName = '虎哥'
#     Client.ID = '6666'
#     Client.registerID = '6666'
#     Client.groupList = ['杀马特团长','虎哥粉丝群','东北沈阳好果汁有限公司']
#     main = Main(Client)
#     main.show()
#     sys.exit(app.exec_())
