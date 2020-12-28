import socket
import threading
import time
import queue
from audioCore import AUDIOSERVER, AUDIOCLIENT
from fileCore import FILECLIENT, FILESERVER

# serverIP = '127.0.0.1'
serverIP = '192.168.43.205'
serverPort = 1919
# audioPort = 8087
audioConnectPort = 8086
filePort = 8088
# fileConnectPort = 8089

audioPort = 8086
# audioConnectPort = 8087
# filePort = 8089
fileConnectPort = 8088


class clientError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


class heartBeatPackage():
    def __init__(self, socketTarget):
        self.socketTarget = socketTarget
        self.stopBeatFlag = 0

    def changeBeatStatus(self, args='STOP'):
        if (args == 'STOP'):
            self.stopBeatFlag = 1
        else:
            self.stopBeatFlag = 0

    def sendTarget(self):
        while True:
            if self.stopBeatFlag == 0:
                self.socketTarget.send(bytes(1))
                time.sleep(8)


class CLIENTCORE():

    def __init__(self):
        # self.localIP = socket.gethostbyname(socket.gethostname())
        # self.localIP = '192.168.43.205'
        self.localIP = '127.0.0.1'
        self.link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.link.connect((serverIP, serverPort))
        # 启动心跳包
        self.heartBeat = heartBeatPackage(self.link)
        self.heartBeatThread = threading.Thread(
            target=self.heartBeat.sendTarget)
        self.heartBeatThread.setDaemon(True)
        self.heartBeatThread.start()
        # 消息队列线程
        self.messageQueue = queue.Queue()
        self.messageThread = threading.Thread(target=self.waitString)
        self.messageThread.setDaemon(True)
        self.messageThread.start()
        self.sendToFrontQueue = queue.Queue()
        self.newBuildGroupQueue = queue.Queue()
        # 指令接受线程
        self.messageEvent = threading.Event()
        self.sendToFrontEvent = threading.Event()
        self.orderThread = threading.Thread(target=self.receiveOrder)
        self.orderThread.setDaemon(True)
        self.orderThread.start()
        # 通话服务器设置
        self.audioServer = AUDIOSERVER(self.localIP, self, audioPort)
        self.fileServer = FILESERVER(self.localIP, filePort, self)
        # 文件服务器设置
        # self.audioServer = AUDIOSERVER('192.168.43.205', self)
        # 其他变量
        self.registerID = ''
        self.ID = ''
        self.userName = ''
        self.groupList = []
        self.requireCallingTarget = ''
        self.callingIP = ''
        self.callingPos = 'slave'
        self.filePath = ''
        self.fileTarget = ''

    def waitString(self):
        while True:
            string = self.link.recv(65536).decode('utf8')
            # print(string)
            self.messageQueue.put(string)
            self.messageEvent.set()

    def receiveOrder(self):
        while True:
            self.messageEvent.wait()
            try:
                while self.messageQueue.empty() != True:
                    string = self.messageQueue.get()
                    stringList = string.split('$')

                    if stringList[0] == 'AskingCalling':
                        self.requireCallingTarget = stringList[1]
                        self.sendToFrontQueue.put('AskingCalling')
                        self.sendToFrontEvent.set()
                        self.callingPos = 'slave'  # 服务器
                        self.audioServer.breakFlag = False

                    elif stringList[0] == 'ReceiveCallingIP':
                        self.callingIP = stringList[1]
                        self.audioClient = AUDIOCLIENT(
                            self.callingIP, audioConnectPort, self)
                        self.sendToFrontQueue.put('ReceiveCalling')
                        self.sendToFrontEvent.set()
                        self.callingPos = 'master'  # 客户端
                        self.audioClient.breakFlag = False

                    elif stringList[0] == 'PassRefuseCalling':
                        self.callingIP = ''
                        self.requireCallingTarget = ''
                        self.sendToFrontQueue.put('PassRefuseCalling')
                        self.sendToFrontEvent.set()

                    elif stringList[0] == 'CallingEnd':
                        self.callingIP = ''
                        self.requireCallingTarget = ''
                        self.audioClient = None
                        self.sendToFrontQueue.put('CallingEnd')
                        self.sendToFrontEvent.set()

                    elif stringList[0] == 'CallingBreak':
                        self.callingIP = ''
                        self.requireCallingTarget = ''
                        self.sendToFrontQueue.put('CallingEnd')
                        self.sendToFrontEvent.set()

                    elif stringList[0] == 'FileSendingIP':
                        self.fileIP = stringList[1]
                        self.fileClient = FILECLIENT(
                            self.fileIP, fileConnectPort, self.filePath, self)

                    elif stringList[0] == 'FileEnd':
                        self.fileIP = ''
                        self.fileTarget = ''
                        self.fileClient = None
                        self.sendToFrontQueue.put('FileEnd')
                        self.sendToFrontEvent.set()
                        self.link.send('FileSendingClose'.encode('utf8'))

                    elif stringList[0] == 'PassFileSending':
                        self.fileTarget = stringList[1]
                        self.sendToFrontQueue.put('PassFileSending')
                        self.sendToFrontEvent.set()
                        self.fileServer.starFile()

                    elif stringList[0] == 'UserName':
                        self.userName = stringList[1]

                    elif stringList[0] == 'GroupMessage':
                        self.sendToFrontQueue.put(string)
                        self.sendToFrontEvent.set()

                    elif stringList[0] == 'RegisterID':
                        self.registerID = stringList[1]

                    elif stringList[0] == 'NewGroupID':
                        self.newBuildGroupQueue.put(stringList[1])

                    elif stringList[0] == 'UserGroupListRefresh':
                        for i in range(1, len(stringList)):
                            cache = stringList[i].split('%')
                            if (not (cache in self.groupList)) and (cache != ['']):
                                self.groupList.append(cache)
                        self.sendToFrontQueue.put('UserGroupListRefresh')
                        self.sendToFrontEvent.set()

                    elif stringList[0] == 'FatalFalse':
                        raise clientError('致命错误')

                    else:
                        self.messageQueue.put(string)
                self.messageEvent.clear()
            except Exception:
                print('error')
                continue

    def refreshGroupList(self):
        try:
            successRecv = False
            self.link.send('RefreshGroupList$'.encode('utf8'))
            while not successRecv:
                string: str = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'UserGroupList':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            for i in range(1, len(stringList)):
                cache = stringList[i].split('%')
                if (not (cache in self.groupList)) and (cache != ['']):
                    self.groupList.append(cache)
            self.sendToFrontQueue.put('UserGroupListRefresh')
            self.sendToFrontEvent.set()
        except Exception:
            print('Timeout')

    def login(self, ID, psd, ipAddr):
        try:
            self.link.send(('LoginRequest$' + ID + '$' +
                            psd + '$' + ipAddr).encode('utf8'))
            loginSuccess = False
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'LoginRequest':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'True':
                loginSuccess = True
                self.ID = ID
                # self.refreshGroupList()
            return loginSuccess
        except Exception:
            return False

    def register(self, ID, psd):
        try:
            self.link.send(
                ('RegisterRequest$' + ID + '$' + psd).encode('utf8'))
            registerSuccess = False
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'RegisterRequest':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'True':
                registerSuccess = True
            return registerSuccess
        except Exception:
            return False

    def sendMessage(self, message, groupID):
        try:
            self.link.send(('SendMessage$' + groupID +
                            '$' + message).encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'SendMessage':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            return (stringList[1] == 'True')
        except Exception:
            return False

    def buildGroup(self, groupName):
        try:
            self.link.send(('BuildGroup$' + groupName).encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'BuildGroup':
                    self.messageQueue.put(string)
                else:
                    successRecv = True
            successRecv = False
            if stringList[1] == 'True':
                while not successRecv:
                    string = self.newBuildGroupQueue.get(True, timeout=2)
                    self.addGroup(self.ID, string)
                    successRecv = True
            return (stringList[1] == 'True')
        except Exception:
            return False

    def addGroup(self, userID, groupID):
        try:
            self.link.send(
                ('AddGroup$' + groupID + '$' + userID).encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'AddGroup':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'True' and userID != self.ID:
                self.refreshGroupList()
            return (stringList[1] == 'True')
        except Exception:
            return False

    def requireCalling(self, targetID):
        try:
            self.link.send(('RequireCalling$' + targetID).encode('utf8'))
            self.requireCallingTarget = targetID
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'RequireCalling':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            return (stringList[1] == 'True')
        except Exception:
            return False

    def closeCalling(self):
        try:
            self.link.send('CloseCalling$'.encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'CloseCalling':
                    self.messageQueue.put(string)
                else:
                    successRecv = True
            if stringList[1] == 'True':
                if self.callingPos == 'master':
                    self.audioClient.closeAudio()
                else:
                    self.audioServer.closeAudio()
                self.messageQueue.put('CallingEnd')
                self.messageEvent.set()
            return (stringList[1] == 'True')
        except Exception:
            return False

    def receiveCalling(self):
        try:
            self.link.send('ReceiveCalling'.encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'ReceiveCalling':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'True':
                self.audioServer.startAudio()
                self.sendToFrontQueue.put('ReceiveCalling')
                self.sendToFrontEvent.set()

            return (stringList[1] == 'True')
        except Exception:
            return False

    def refuseCalling(self):
        try:
            self.link.send('RefuseCalling$'.encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'RefuseCalling':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            return (stringList[1] == 'True')
        except Exception:
            return False

    def sendFile(self, filePath, targetID):
        try:
            self.filePath = filePath
            self.link.send(('FileSending$' + targetID).encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True, timeout=2)
                stringList = string.split('$')
                if stringList[0] != 'FileSending':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'False':
                return False
            else:
                self.fileTarget = targetID
                self.messageQueue.put('FileSendingIP$' + stringList[1])
                self.messageEvent.set()
                return True

        except Exception:
            return False


# SOC = CLIENTCORE()
# while True:
#     string = input()
#     stringList = string.split('$')
#     if stringList[0].find('R') != -1:
#         SOC.register(stringList[1],stringList[2])
#     elif stringList[0].find('L') != -1:
#         SOC.login(stringList[1],stringList[2],stringList[3])
#     elif stringList[0].find('B') != -1:
#         SOC.buildGroup(stringList[1])
#     elif stringList[0].find('A') != -1:
#         SOC.addGroup(stringList[1], stringList[2])
#     elif stringList[0].find('S') != -1:
#         SOC.sendMessage(stringList[1],stringList[2])
#     elif stringList[0].find('P') != -1:
#         print(SOC.groupList)
#     elif stringList[0].find('I') != -1:
#         SOC.link.send(input().encode('utf8'))
