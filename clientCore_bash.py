import socket
import threading
import time
import queue

serverIP = '127.0.0.1'
serverPort = 1919

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
        self.link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.link.connect((serverIP, serverPort))
        # 启动心跳包
        self.heartBeat = heartBeatPackage(self.link)
        self.heartBeatThread = threading.Thread(target=self.heartBeat.sendTarget)
        self.heartBeatThread.setDaemon(True)
        self.heartBeatThread.start()
        # 消息队列线程
        self.messageQueue = queue.Queue()
        self.messageThread = threading.Thread(target=self.waitString)
        self.messageThread.setDaemon(True)
        self.messageThread.start()
        # 指令接受线程
        self.orderThread = threading.Thread(target=self.receiveOrder)
        self.orderThread.setDaemon(True)
        self.orderThread.start()
        # 其他变量
        self.registerID = ''
        self.ID = ''
        self.userName = ''
        self.newBuildGroupQueue = queue.Queue()
        self.groupList = []
        self.sendToFrontQueue = queue.Queue()
        self.requireCallingTarget = ''
        
    def waitString(self):
        while True:
            string = self.link.recv(65536).decode('utf8')
            print(string)
            self.messageQueue.put(string)

    def receiveOrder(self):
        while True:
            try:
                if self.messageQueue.empty() != True:
                    string = self.messageQueue.get()
                    stringList = string.split('$')

                    if stringList[0] == 'RequireCalling':
                        self.requireCallingTarget = stringList[1]
                        self.sendToFrontQueue.put('RequireCalling')

                    elif stringList[0] == 'UserName':
                        self.userName = stringList[1]
                        self.sendToFrontQueue.put('UserName')

                    elif stringList[0] == 'GroupMessage':
                        self.sendToFrontQueue.put(string)

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

                    elif stringList[0] == 'FatalFalse':
                        raise clientError('致命错误')

                    else:
                        self.messageQueue.put(string)

            except Exception:
                print('error')
                continue

    def refreshGroupList(self):
        try:
            successRecv = False
            self.link.send('RefreshGroupList$'.encode('utf8'))
            while not successRecv:
                string = self.messageQueue.get(True,timeout=5)
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
        except Exception:
            print('Timeout')

    def login(self, ID, psd, ipAddr):
        try:
            self.link.send(('LoginRequest$' + ID + '$' +psd + '$' + ipAddr).encode('utf8'))
            loginSuccess = False
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True,timeout=5)
                stringList = string.split('$')
                if stringList[0] != 'LoginRequest':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'True':
                loginSuccess = True
                self.ID = ID
                self.refreshGroupList()
            return loginSuccess
        except Exception:
            return

    def register(self, ID, psd):
        try:
            self.link.send(('RegisterRequest$' + ID + '$' + psd).encode('utf8'))
            registerSuccess = False
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True,timeout=5)
                stringList = string.split('$')
                if stringList[0] != 'RegisterRequest':
                    self.messageQueue.put(string)
                else:
                    successRecv = True
                
            if stringList[1] == 'True':
                registerSuccess = True
            return registerSuccess
        except Exception:
            return

    def sendMessage(self, message, groupID):
        self.link.send(('SendMessage$' + groupID +'$' + message).encode('utf8')) 

    def buildGroup(self, groupName):
        try:
            self.link.send(('BuildGroup$' + groupName).encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True,timeout=5)
                stringList = string.split('$')
                if stringList[0] != 'BuildGroup':
                    self.messageQueue.put(string)
                else:
                    successRecv = True
            successRecv = False
            if stringList[1] == 'True':
                while not successRecv:
                    string = self.newBuildGroupQueue.get(True,timeout=5)
                    self.addGroup(self.ID, string)
                    successRecv = True
            return (stringList[1] == 'True')
        except Exception:
            return

    def addGroup(self, userID, groupID):
        try:
            self.link.send(('AddGroup$' + groupID + '$' + userID).encode('utf8'))
            successRecv = False
            while not successRecv:
                string = self.messageQueue.get(True,timeout=5)
                stringList = string.split('$')
                if stringList[0] != 'AddGroup':
                    self.messageQueue.put(string)
                else:
                    successRecv = True

            if stringList[1] == 'True' and userID != self.ID:
                self.refreshGroupList()
            return (stringList[1] == 'True')
        except Exception:
            return


SOC = CLIENTCORE()
while True:
    string = input()
    stringList = string.split('$')
    if stringList[0].find('R') != -1:
        SOC.register(stringList[1],stringList[2])
    elif stringList[0].find('L') != -1:
        SOC.login(stringList[1],stringList[2],stringList[3])
    elif stringList[0].find('B') != -1:
        SOC.buildGroup(stringList[1])
    elif stringList[0].find('A') != -1:
        SOC.addGroup(stringList[1], stringList[2])
    elif stringList[0].find('S') != -1:
        SOC.sendMessage(stringList[1],stringList[2])
    elif stringList[0].find('P') != -1:
        print(SOC.groupList)
    elif stringList[0].find('I') != -1:
        SOC.link.send(input().encode('utf8'))
