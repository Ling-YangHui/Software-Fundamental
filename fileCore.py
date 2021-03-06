import threading
import os
import sys
import socket
import json


class FILESERVER:

    def __init__(self, IP, port, client):
        self.fileServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileServer.bind((IP, port))
        self.fileServer.listen(16)
        self.clientCore = client

    def starFile(self):
        self.connect, address = self.fileServer.accept()
        self.receivedSize = 0
        # 设置文件存储路径，为与该程序同目录的Data文件夹
        self.storePath = os.path.abspath('.') + '\Data'
        # 设置每次接收量
        self.receiveSize = 1024

        self.fileIn = threading.Thread(target=self.getFile)
        self.fileIn.setDaemon = True
        self.fileIn.start()

    def getFile(self):
        try:
            # 接收文件名与大小
            self.jsonString = self.connect.recv(2048)
            self.jsonDictionary = json.loads(self.jsonString.decode())
            print('文件大小: {} kb, 开始接收'.format(self.jsonDictionary['size'] / 1024))
            # 编写新文件绝对路径
            path = os.path.join(self.storePath, self.jsonDictionary["name"])
            self.filePath = os.path.join(
                self.storePath, self.jsonDictionary["name"])
            isNewFile = False
            num = 1
            
            name:str = self.jsonDictionary['name']
            nameWithoutExternList = name.split('.')
            nameWithoutExtern = ''
            nameExtern = ''
            for i in range(len(nameWithoutExternList) - 1):
                nameWithoutExtern += nameWithoutExternList[i]
            if len(nameWithoutExternList) != 1:
                nameExtern = nameWithoutExternList[-1]

            while not isNewFile:
                try:
                    file = open(self.filePath, 'r')
                except Exception:
                    isNewFile = True
                if isNewFile == False:
                    name = nameWithoutExtern + '(' + str(num) + ')' + nameExtern
                    self.filePath = os.path.join(self.storePath, name)
                    num += 1
            # 向客户端发送可以接收文件内容的信号
            self.connect.send("Ture".encode())
            fileSize = self.jsonDictionary['size']
            with open(self.filePath, 'wb') as file:
                # 开始写文件
                while self.receivedSize < fileSize:
                    cache = self.connect.recv(1024)
                    file.write(cache)
                    self.receivedSize += len(cache)
                    print('接收进度: ' + str(self.receivedSize) + '/' + str(fileSize),end='\r')
        except Exception as E:
            self.clientCore.messageQueue.put('FileEnd')
            self.clientCore.messageEvent.set()
            self.connect.shutdown(socket.SHUT_RDWR)
            self.connect.close()
            print(E)
            return

        self.connect.settimeout(30)
        try:
            self.connect.send(self.jsonDictionary['name'].encode('utf8'))
            string = self.connect.recv(65536).decode('utf8')
            if string == self.jsonDictionary['name']:
                pass
            else:
                print(string)
                print('接收失败')
        except Exception as E:
            print(E)

        print('接收结束')
        self.connect.shutdown(socket.SHUT_RDWR)
        self.connect.close()
        self.clientCore.messageQueue.put('FileEnd')
        self.clientCore.messageEvent.set()


class FILECLIENT:

    def __init__(self, IP, port, filePath, client):
        self.fileClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileClient.connect((IP, port))
        self.clientCore = client
        # 设置每次发送量
        self.sendSize = 1024

        self.fileOut = threading.Thread(target=self.sendFile, args=(filePath,))
        self.fileOut.setDaemon = True
        self.fileOut.start()

    def sendFile(self, filePath):
        self.sentSize = 0
        # 获取文件名与大小
        self.fileName = os.path.basename(filePath)
        self.fileSize = os.path.getsize(filePath)
        # 发送文件名与大小
        print('文件大小: {} kb, 开始发送'.format(self.fileSize / 1024))
        self.jsonDictionary = {"name": self.fileName, "size": self.fileSize}
        self.jsonString = json.dumps(self.jsonDictionary).encode("utf-8")
        try:
            self.fileClient.send(self.jsonString)
            # 等待服务端返回开始信号
            if self.fileClient.recv(100).decode() == 'Ture':
                with open(filePath, 'rb') as file:
                    # 读取文件
                    while self.sentSize < self.fileSize:
                        self.sendSize = self.fileClient.send(file.read(1024))
                        self.sentSize += self.sendSize
                        print('发送进度: ' + str(self.sentSize) + '/' + str(self.fileSize), end='\r')
        except Exception as E:
            self.clientCore.messageQueue.put('FileEnd')
            self.clientCore.messageEvent.set()
            self.fileClient.shutdown(socket.SHUT_RDWR)
            self.fileClient.close()
            print(E)
            return

        self.fileClient.settimeout(30)
        try:
            string = self.fileClient.recv(65536).decode('utf8')
            if string == self.jsonDictionary['name']:
                self.fileClient.send(self.jsonDictionary['name'].encode('utf8'))
            else:
                print(string)
                print('发送失败')
        except Exception as E:
            print(E)

        print('发送结束')
        self.fileClient.shutdown(socket.SHUT_RDWR)
        self.fileClient.close()
        self.clientCore.messageQueue.put('FileEnd')
        self.clientCore.messageEvent.set()
