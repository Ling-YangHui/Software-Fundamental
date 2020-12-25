import threading,os,sys
import socket,json

class FILESERVER:

    def __init__(self,IP,port,client):
        self.fileServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileServer.bind((IP, port))
        self.fileServer.listen(16)
        self.clientCore = client
    
    def starFile(self):
        self.connect, address = self.fileServer.accept()
        self.receivedSize = 0
        #设置文件存储路径，为与该程序同目录的Data文件夹
        self.storePath = os.path.abspath('.') + '\Data'
        #设置每次接收量
        self.receiveSize = 1024

        self.fileIn = threading.Thread(target=self.getFile)
        self.fileIn.setDaemon = True
        self.fileIn.start()
    
    def getFile(self):
        try:
            #接收文件名与大小
            self.jsonString = self.connect.recv(2048)
            self.jsonDictionary = json.loads(self.jsonString.decode())
            #编写新文件绝对路径
            self.filePath = os.path.join(self.storePath,self.jsonDictionary["name"])
            #向客户端发送可以接收文件内容的信号
            self.connect.send("Ture".encode())
            with open(self.filePath,'wb') as file:
                #开始写文件
                while self.receivedSize < self.jsonDictionary["size"]:
                    file.write(self.connect.recv(self.receiveSize))
                    self.receivedSize += self.receiveSize
        except Exception as E:
            self.clientCore.messageQueue.put('FileEnd')
            self.clientCore.messageEvent.set()
            print(E)
            return

        self.clientCore.messageQueue.put('FileEnd')
        self.clientCore.messageEvent.set()
        
        

class FILECLIENT:

    def __init__(self,IP,port,filePath,client):
        self.fileClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileClient.connect((IP, port))
        self.clientCore = client
        #设置每次发送量
        self.sendSize = 1024

        self.fileOut = threading.Thread(target=self.sendFile,args=(filePath,))
        self.fileOut.setDaemon = True
        self.fileOut.start()

    def sendFile(self,filePath):
        self.sentSize = 0
        #获取文件名与大小
        self.fileName = os.path.basename(filePath)
        self.fileSize = os.path.getsize(filePath)
        #发送文件名与大小
        self.jsonDictionary = {"name":self.fileName,"size":self.fileSize}
        self.jsonString = json.dumps(self.jsonDictionary).encode("utf-8")
        try:
            self.fileClient.send(self.jsonString)
            #等待服务端返回开始信号
            if self.fileClient.recv(100).decode() == 'Ture':
                with open(filePath,'rb') as file:
                    #读取文件
                    while self.sentSize < self.fileSize:
                        self.fileClient.send(file.read(1024))
                        self.sentSize += self.sendSize
        except Exception as E:
            self.clientCore.messageQueue.put('FileEnd')
            self.clientCore.messageEvent.set()
            print(E)
            return

        self.clientCore.messageQueue.put('FileEnd')
        self.clientCore.messageEvent.set()
