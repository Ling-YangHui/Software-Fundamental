import threading
import socket
import queue
import random
import json
import traceback


class USERLIST(object):  # 用户列表类

    # 子类
    class USER(object):

        # 为了防止属性出现混连，在USER类中不声明任何私有属性，所有私有属性在__init__里面下载好

        # 用户创建方法
        def __init__(self, Name, PSD, ID):
            self.Name = Name
            self.PSD = PSD
            self.ID = ID
            self.groupList = []
            self.isOnline = False
            self.connect = None  # 链接的对象，为一个socket类对象
            self.status = 'offline'  # 当前的用户自定义状态
            self.selfLock = threading.Lock()  # 对自身信息操作的锁
            self.loginID = 0
            # 用户P2P通信专区
            self.p2pIP = ''
            self.isCalling = False
            self.isFiling = False
            self.waiting = -1  # 请求通话的对面用户ID，通话进行中也复用为正在通话的ID
            self.waitingFile = -1  # 请求发送文件的用户ID，文件发送中也复用为正在发送文件的ID

        def joinGroup(self, groupID):
            try:
                self.selfLock.acquire()
                if not groupID in self.groupList:
                    self.groupList.append(groupID)
                    userJson = {'Name': self.Name, 'PSD': self.PSD,
                                'LoginID': self.loginID, 'GroupList': self.groupList, 'ID': self.ID}
                    jsonList.setUserJson(userJson)
                self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def sendMessageToGroup(self, groupID, message):
            try:
                message = self.Name + '$' + message
                if groupID in self.groupList:
                    groupList.sendMessage(self.ID, message)
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def sendMessageToUser(self, message):
            try:
                if self.isOnline == True:
                    self.selfLock.acquire()
                    self.connect.send(message.encode('utf8'))
                    self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def setOnlineOffline(self, arg='Offline'):
            try:
                if arg == 'Offline':
                    self.selfLock.acquire()
                    self.isOnline = False
                    self.selfLock.release()
                else:
                    self.selfLock.acquire()
                    self.isOnline = True
                    self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def setOnOffCalling(self, arg='offcalling'):
            try:
                if arg == 'offcalling':
                    self.selfLock.acquire()
                    self.isCalling = False
                    self.selfLock.release()
                else:
                    self.selfLock.acquire()
                    self.isCalling = True
                    self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def setWaiting(self, ID):
            try:
                self.selfLock.acquire()
                self.waiting = ID
                self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def setFileWaiting(self, ID):
            try:
                self.selfLock.acquire()
                self.waitingFile = ID
                self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def setFiling(self, arg='offFiling'):
            try:
                self.selfLock.acquire()
                if arg == 'offFiling':
                    self.isFiling = False
                else:
                    self.isFiling = True
                self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def setP2PIP(self, IP):
            try:
                self.selfLock.acquire()
                self.p2pIP = IP
                self.selfLock.release()
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

        def refreshUserGroupList(self, arg='ask'):
            try:
                message = 'UserGroupList$'
                if arg != 'ask':
                    message = 'UserGroupListRefresh$'
                for index in self.groupList:
                    message += str(groupList.ID2searchID(index)) + \
                        '%' + groupList.getName(index) + '$'  # index为群组ID
                self.sendMessageToUser(message)
            except Exception as Error:
                print(traceback.format_exc())
                return False
            return True

    # 列表私有属性
    __userList = []
    __loginIDList = []
    __nextUserID = 0
    __userListLock = threading.Lock()

    # 列表的操作类方法
    def regNewUser(self, Name, PSD):
        # 创建一个newUser对象
        try:
            NewUser = self.USER(Name, PSD, self.__nextUserID)
            self.__nextUserID += 1
            loginID = random.randint(1000, 9999)
            while loginID in self.__loginIDList:
                loginID = random.randint(1000, 9999)
            NewUser.loginID = loginID
            self.__userListLock.acquire()
            self.__userList.append(NewUser)
            self.__loginIDList.append(loginID)
            self.__userListLock.release()

            newUserDict = {'Name': Name, 'PSD': PSD,
                           'ID': self.__nextUserID - 1, 'LoginID': loginID, 'GroupList': []}
            jsonList.setUserJson(newUserDict, new=True)
        # 任何错误都要抛出一个异常，并且表示运行执行错误
        except Exception as Error:
            print(traceback.format_exc())
            return -1
        return loginID

    def setUserList(self):
        userJsonList = jsonList.getUserJson()
        for index in userJsonList:
            NewUser = self.USER(index['Name'], index['PSD'], self.__nextUserID)
            NewUser.groupList = index['GroupList']
            NewUser.loginID = index['LoginID']
            self.__userList.append(NewUser)
            self.__loginIDList.append(index['LoginID'])
            self.__nextUserID += 1

    def userLogin(self, ID, PSD, connect):
        # 直接查找对应的列表，捕捉indexError
        try:
            if self.__userList[ID].PSD == PSD:
                self.__userList[ID].connect = connect
                self.__userList[ID].isOnline = True
                # self.refreshUserGroupList(self.__userList[ID].ID)
                return True
            else:
                return False
        except IndexError as Error:
            print(traceback.format_exc())
            return False

    def refreshUserGroupList(self, ID, arg='ask'):
        return self.__userList[ID].refreshUserGroupList(arg=arg)

    def joinGroup(self, ID, groupID):
        return self.__userList[ID].joinGroup(groupID)

    def sendMessageToUser(self, ID, message):
        return self.__userList[ID].sendMessageToUser(message)

    def sendMessageToGroup(self, ID, groupID, message):
        return self.__userList[ID].sendMessageToGroup(groupID, message)

    def setOnline(self, ID):
        return self.__userList[ID].setOnlineOffline(arg='Online')

    def setOffline(self, ID):
        return self.__userList[ID].setOnlineOffline(arg='Offline')

    def setP2PIP(self, ID, IP):
        return self.__userList[ID].setP2PIP(IP)

    def setOnCalling(self, ID):
        return self.__userList[ID].setOnOffCalling(arg='oncalling')

    def setOffCalling(self, ID):
        return self.__userList[ID].setOnOffCalling(arg='offcalling')

    def setWaiting(self, ID, targetID):
        return self.__userList[ID].setWaiting(targetID)

    def setFileWaiting(self, ID, targetID):
        return self.__userList[ID].setFileWaiting(targetID)

    def setOffFiling(self, ID):
        return self.__userList[ID].setFiling(arg='offFiling')

    def setOnFiling(self, ID):
        return self.__userList[ID].setFiling(arg='onFiling')

    # 服务类方法
    def loginID2ID(self, loginID):
        try:
            return self.__loginIDList.index(loginID)
        except Exception:
            print(traceback.format_exc())
            return -2

    def ID2LoginID(self, ID):
        return self.__loginIDList[ID]

    def getName(self, ID):
        return self.__userList[ID].Name

    def getOnline(self, ID):
        return self.__userList[ID].isOnline

    def getGroupList(self, ID):
        return self.__userList[ID].groupList

    def findIDValid(self, ID):
        return ID < len(self.__userList) and ID >= 0

    def getCalling(self, ID):
        return self.__userList[ID].isCalling

    def getP2PIP(self, ID):
        return self.__userList[ID].p2pIP

    def getFiling(self, ID):
        return self.__userList[ID].isFiling

    def getWaitingTarget(self, ID):
        return self.__userList[ID].waiting

    def getWaitingFileTarget(self, ID):
        return self.__userList[ID].waitingFile


class GROUPLIST(object):  # 群聊组表类

    # 子类
    class GROUP(object):

        # 为了防止属性出现混连，在USER类中不声明任何私有属性，所有私有属性在__init__里面下载好

        def __init__(self, Name, ID):
            self.Name = Name
            self.ID = ID
            self.memberList = []
            self.joinQueue = queue.Queue(maxsize=0)  # 加入队列，自带线程安全
            self.messageQueue = queue.Queue(maxsize=0)  # 消息队列，自带线程安全
            self.searchID = 0
            self.groupEvent = threading.Event()
            self.groupEvent.clear()

        def serveThreadFunction(self):
            while(True):
                self.groupEvent.wait()
                self.joinMembers()
                self.sendMessage()
                self.groupEvent.clear()

        def joinMembers(self):  # 监听添加一个群组列表成员
            while (self.joinQueue.empty() == False):
                ID = self.joinQueue.get()
                if ID in self.memberList:
                    continue
                self.memberList.append(ID)
                groupJson = {'ID': self.ID, 'SearchID': self.searchID,
                             'MemberList': self.memberList, 'Name': self.Name}
                jsonList.setGroupJson(groupJson)

        def sendMessage(self):
            while (self.messageQueue.empty() == False):
                message = self.messageQueue.get()
                message = 'GroupMessage$' + \
                    str(groupList.ID2searchID(self.ID)) + \
                    '$' + self.Name + '$' + message
                for i in self.memberList:
                    userList.sendMessageToUser(i, message)

    # 私有属性
    __groupList = []  # 群组列表，元素为子类GROUP的实例
    __searchIDList = []  # 群组索引表
    __nextGroupID = 0
    __groupListLock = threading.Lock()  # 群组列表线程锁
    __groupThreadList = []  # 群组维持线程池

    # 列表的操作类方法
    def buildNewGroup(self, Name):
        # 创建一个newGroup对象
        try:
            newGroup = self.GROUP(Name, self.__nextGroupID)
            self.__nextGroupID += 1
            newGroupThread = threading.Thread(
                target=newGroup.serveThreadFunction)
            newGroupThread.setDaemon(True)
            newGroupThread.start()

            searchID = random.randint(100, 999)
            while searchID in self.__searchIDList:
                searchID = random.randint(100, 999)
            newGroup.searchID = searchID
            self.__groupListLock.acquire()
            self.__searchIDList.append(searchID)
            self.__groupList.append(newGroup)
            self.__groupThreadList.append(newGroupThread)
            self.__groupListLock.release()

            groupJson = {'Name': Name, 'ID': self.__nextGroupID -
                         1, 'MemberList': [], 'SearchID': searchID}
            jsonList.setGroupJson(groupJson, new=True)

        except Exception as Error:
            print(traceback.format_exc())
            return -2
        return searchID

    def setGroupList(self):
        groupJsonList = jsonList.getGroupJson()
        for index in groupJsonList:
            newGroup = self.GROUP(index['Name'], index['ID'])
            self.__nextGroupID += 1
            newGroup.memberList = index['MemberList']
            newGroup.searchID = index['SearchID']
            newGroupThread = threading.Thread(
                target=newGroup.serveThreadFunction)
            newGroupThread.setDaemon(True)
            newGroupThread.start()

            self.__searchIDList.append(index['SearchID'])
            self.__groupList.append(newGroup)
            self.__groupThreadList.append(newGroupThread)

    def sendMessage(self, ID, message):
        try:
            self.__groupList[ID].messageQueue.put(message)
            self.__groupList[ID].groupEvent.set()
        except Exception as Error:
            print(traceback.format_exc())
            return False
        return True

    def joinMembers(self, ID, userID):
        try:
            self.__groupList[ID].joinQueue.put(userID)
            self.__groupList[ID].groupEvent.set()
        except Exception as Error:
            print(traceback.format_exc())
            return False
        return True

    # 服务类方法
    def getName(self, ID):
        return self.__groupList[ID].Name

    def findIDValid(self, ID):
        return ID < len(self.__groupList) and ID >= 0

    def searchID2ID(self, searchID):
        try:
            return self.__searchIDList.index(searchID)
        except Exception:
            print(traceback.format_exc())
            return -2

    def ID2searchID(self, ID):
        try:
            return self.__searchIDList[ID]
        except Exception:
            print(traceback.format_exc())
            return -2


class LINKLIST(object):

    # 子类
    class LINK(object):

        # 为了防止属性出现混连，在USER类中不声明任何私有属性，所有私有属性在__init__里面下载好

        def __init__(self, connect):  # 初始化一个连接
            self.__connect: socket = connect
            self.__userID = -1
            self.__userName = ''

        def sendFalse(self, string):
            self.__connect.send((string + '$False').encode('utf8'))

        def sendTrue(self, string):
            self.__connect.send((string + '$True').encode('utf8'))

        def listenCommand(self):  # 一个单独运行的线程，对对应的connect进行监听
            self.__connect.settimeout(10000)  # 设置超时
            while True:
                try:
                    stringByte: bytes = self.__connect.recv(65536)
                    string: bytearray = bytearray(stringByte)
                    string = string.replace(b'\x00', b'')
                    string: str = string.decode('utf8')
                    if string == '':
                        continue

                    print(string)

                    orderList = string.split('$')
                    if orderList[0] == 'RegisterRequest':  # 处理注册请求 只有在注册请求的时候才可以修改用户列表的数值
                        # Name PSD
                        loginID = userList.regNewUser(
                            orderList[1], orderList[2])
                        if loginID == -1:
                            self.sendFalse('RegisterRequest')
                        else:
                            self.__connect.send(
                                ('RegisterID$' + str(loginID)).encode('utf8'))  # 把获取到的ID回传回去
                            self.sendTrue('RegisterRequest')

                    elif orderList[0] == 'LoginRequest':  # 处理登陆请求
                        # LoginID PSD IP
                        if userList.userLogin(userList.loginID2ID(int(orderList[1])), orderList[2], self.__connect) == False:
                            self.sendFalse('LoginRequest')
                        else:
                            self.__userID = userList.loginID2ID(
                                int(orderList[1]))
                            self.__userName = userList.getName(self.__userID)
                            userList.setP2PIP(self.__userID, orderList[3])
                            self.sendTrue('LoginRequest')
                            userList.sendMessageToUser(
                                self.__userID, 'UserName$' + self.__userName)

                    elif orderList[0] == 'BuildGroup' and self.__userID != -1:  # 处理建群请求
                        # GName
                        searchID = groupList.buildNewGroup(orderList[1])
                        if searchID == -2:
                            self.sendFalse('BuildGroup')
                        else:
                            self.sendTrue('BuildGroup')
                            userList.sendMessageToUser(
                                self.__userID, 'NewGroupID$' + str(searchID))

                    elif orderList[0] == 'AddGroup' and self.__userID != -1:  # 处理加群请求
                        # GID LoginID
                        ID = userList.loginID2ID(int(orderList[2]))
                        GID = groupList.searchID2ID(int(orderList[1]))
                        if (not userList.findIDValid(ID)) or (not groupList.findIDValid(GID)):
                            self.sendFalse('AddGroup')
                        elif groupList.joinMembers(GID, ID) == False:
                            self.sendFalse('AddGroup')
                        else:
                            userList.joinGroup(ID, GID)
                            userList.refreshUserGroupList(ID, 'not ask')
                            self.sendTrue('AddGroup')

                    elif orderList[0] == 'RefreshGroupList' and self.__userID != -1:
                        userList.refreshUserGroupList(self.__userID)

                    elif orderList[0] == 'SendMessage' and self.__userID != -1:  # 处理发送请求
                        # GID Message
                        groupListCache = userList.getGroupList(self.__userID)
                        GID = groupList.searchID2ID(int(orderList[1]))
                        if GID in groupListCache:
                            text = ''
                            for index in range(2, len(orderList)):
                                text += orderList[index]
                                text += '$'
                            message = self.__userName + '$' + text
                            if groupList.sendMessage(GID, message) == True:
                                self.sendTrue('SendMessage')
                            else:
                                self.sendFalse('SendMessage')
                        else:
                            self.sendFalse('SendMessage')

                    elif orderList[0] == 'RequireCalling' and self.__userID != -1:  # 处理p2p通话请求
                        # Target
                        targetID = userList.loginID2ID(int(orderList[1]))
                        if not userList.findIDValid(targetID):
                            self.sendFalse('RequireCalling')
                            return
                        if userList.getCalling(targetID) == True:
                            self.sendFalse('RequireCalling')
                        if userList.getOnline(targetID) == False:
                            self.sendFalse('RequireCalling')
                        else:
                            userList.sendMessageToUser(
                                targetID, 'AskingCalling$' + str(userList.ID2LoginID(self.__userID)))
                            userList.setWaiting(self.__userID, targetID)
                            userList.setWaiting(targetID, self.__userID)
                            userList.setOnCalling(targetID)  # 声明进入通讯模式，其余不可接入
                            userList.setOnCalling(self.__userID)
                            self.sendTrue('RequireCalling')

                    elif orderList[0] == 'CloseCalling' and self.__userID != -1:
                        # 关闭双方占线状态
                        userList.setOffCalling(self.__userID)
                        userList.setOffCalling(
                            userList.getWaitingTarget(self.__userID))
                        # 发送关闭指令
                        userList.sendMessageToUser(
                            userList.getWaitingTarget(self.__userID), 'CallingEnd$')
                        # 消除通话对象
                        targetID = userList.getWaitingTarget(self.__userID)
                        userList.setWaiting(self.__userID, -1)
                        userList.setWaiting(targetID, -1)
                        self.sendTrue('CloseCalling')

                    elif orderList[0] == 'ReceiveCalling' and self.__userID != -1:
                        # 发送IP包
                        userList.sendMessageToUser(userList.getWaitingTarget(
                            self.__userID), 'ReceiveCallingIP$' + userList.getP2PIP(self.__userID))
                        self.sendTrue('ReceiveCalling')

                    elif orderList[0] == 'RefuseCalling' and self.__userID != -1:
                        # 关闭双方占线状态
                        userList.setOffCalling(self.__userID)
                        userList.setOffCalling(
                            userList.getWaitingTarget(self.__userID))
                        # 发送拒绝代码
                        userList.sendMessageToUser(
                            userList.getWaitingTarget(self.__userID), 'PassRefuseCalling$')
                        # 消除通话对象
                        targetID = userList.getWaitingTarget(self.__userID)
                        userList.setWaiting(self.__userID, -1)
                        userList.setWaiting(targetID, -1)
                        self.sendTrue('RefuseCalling')

                    elif orderList[0] == 'FileSending' and self.__userID != -1:
                        targetID = userList.loginID2ID(int(orderList[1]))
                        if userList.findIDValid(targetID) == False:
                            self.sendFalse('FileSending')
                        if userList.getOnline(targetID) == False:
                            self.sendFalse('FileSending')
                        if userList.getFiling(targetID) == True:
                            self.sendFalse('FileSending')
                        else:
                            userList.setFileWaiting(self.__userID, targetID)
                            userList.setFileWaiting(targetID, self.__userID)
                            userList.setOnFiling(targetID)
                            userList.setOnFiling(self.__userID)
                            userList.sendMessageToUser(
                                targetID, 'PassFileSending$' + str(userList.ID2LoginID(self.__userID)))
                            userList.sendMessageToUser(
                                self.__userID, 'FileSending$' + userList.getP2PIP(targetID))

                    elif orderList[0] == 'FileSendingClose' and self.__userID != -1:
                        # 关闭占线状态
                        userList.setOffFiling(self.__userID)
                        userList.setOffFiling(
                            userList.getWaitingFileTarget(self.__userID))
                        # 发送关闭指令
                        # userList.sendMessageToUser(
                        #     self.__userID, 'FileSendingClose$')
                        # userList.sendMessageToUser(userList.getWaitingFileTarget(
                        #     self.__userID), 'FileSendingClose$')
                        # 消除通话对象
                        targetID = userList.getWaitingFileTarget(self.__userID)
                        userList.setFileWaiting(self.__userID, -1)
                        userList.setFileWaiting(targetID, -1)

                # 连接出现错误
                except socket.timeout:
                    print('TimeoutError')
                    if (self.__userID != -1):
                        userList.setOffline(self.__userID)
                        if userList.getCalling(self.__userID):
                            userList.setOffCalling(self.__userID)
                            userList.setOffCalling(
                                userList.getCalling(self.__userID))
                        if userList.getFiling(self.__userID):
                            userList.setOffFiling(self.__userID)
                            userList.setOffFiling(
                                userList.getFiling(self.__userID))
                    nowThread = threading.current_thread()
                    linkList.delLinkThread(nowThread)
                    break
                except ConnectionResetError:
                    print('ConnectionLose')
                    if self.__userID != -1:
                        userList.setOffline(self.__userID)
                        if userList.getCalling(self.__userID):
                            userList.setOffCalling(self.__userID)
                            userList.setOffCalling(
                                userList.getCalling(self.__userID))
                        if userList.getFiling(self.__userID):
                            userList.setOffFiling(self.__userID)
                            userList.setOffFiling(
                                userList.getFiling(self.__userID))
                    nowThread = threading.current_thread()
                    linkList.delLinkThread(nowThread)
                    break

                # 操作形式错误
                except Exception as Error:
                    print(traceback.format_exc())
                    self.__connect.send('FatalFalse$'.encode('utf8'))

    __linkThreadList = []

    def listenNewLink(self):  # 实时运行的main线程，用于监听新的连接的存在
        while True:
            connect, address = SOC.accept()
            link = self.LINK(connect)
            linkThread = threading.Thread(target=link.listenCommand)
            linkThread.setDaemon(True)
            linkThread.start()
            self.__linkThreadList.append(linkThread)

    def delLinkThread(self, thread):
        self.__linkThreadList.remove(thread)


class JSONLIST(object):

    def __init__(self):
        self.userJsonFilePath = 'userInfo.json'
        file = open(self.userJsonFilePath, 'r')
        self.userJsonList: list
        self.userJsonList = json.load(file)
        self.userJsonList.sort(key=self.sortKey)
        file.close()
        self.userListLock = threading.Lock()

        self.groupJsonFilePath = 'groupInfo.json'
        file = open(self.groupJsonFilePath, 'r')
        self.groupJsonList: list
        self.groupJsonList = json.load(file)
        self.groupJsonList.sort(key=self.sortKey)
        file.close()
        self.groupListLock = threading.Lock()

    def sortKey(self, jsonItem):
        return jsonItem['ID']

    def getUserJson(self):
        return self.userJsonList

    def setUserJson(self, newUser, new=False):
        newFlag = True
        if not new:
            for i in range(0, len(self.userJsonList)):
                if self.userJsonList[i]['ID'] == newUser['ID']:
                    self.userListLock.acquire()
                    self.userJsonList[i] = newUser
                    self.userListLock.release()
                    newFlag = False
                    break
        if newFlag:
            self.userListLock.acquire()
            self.userJsonList.append(newUser)
            self.userListLock.release()
        self.userListLock.acquire()
        with open(self.userJsonFilePath, 'w') as file:
            json.dump(self.userJsonList, file)
        self.userListLock.release()

    def getGroupJson(self):
        return self.groupJsonList

    def setGroupJson(self, newGroup, new=False):
        newFlag = True
        if not new:
            for i in range(0, len(self.groupJsonList)):
                if self.groupJsonList[i]['ID'] == newGroup['ID']:
                    self.groupListLock.acquire()
                    self.groupJsonList[i] = newGroup
                    self.groupListLock.release()
                    newFlag = False
                    break
        if newFlag:
            self.groupListLock.acquire()
            self.groupJsonList.append(newGroup)
            self.groupListLock.release()
        self.groupListLock.acquire()
        with open(self.groupJsonFilePath, 'w') as file:
            json.dump(self.groupJsonList, file)
        self.groupListLock.release()


# 监听初始化
IP = '127.0.0.1'
# IP = '192.168.43.205'
port = 1919

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 设置socket模式
SOC.bind((IP, port))  # 绑定IP和port
SOC.listen(1024)  # 最大监听量1024

userList = USERLIST()
groupList = GROUPLIST()
linkList = LINKLIST()
jsonList = JSONLIST()
userList.setUserList()
groupList.setGroupList()

linkList.listenNewLink()
