import socket
import threading
import pyaudio


class AUDIOSERVER:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1

    def __init__(self, IP):
        self.audioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audioServer.bind((IP, 8086))
        self.audioServer.listen(1)
        self.breakFlag = False

    def startAudio(self):
        self.connect, address = self.audioServer.accept()
        self.pyAU = pyaudio.PyAudio()
        self.audioInputStream = self.pyAU.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          frames_per_buffer=self.CHUNK)
        self.audioOutputStream = self.pyAU.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          output=True,
                                          frames_per_buffer=self.CHUNK)

        self.audioInThread = threading.Thread(target=self.collectAudio)
        self.audioInThread.setDaemon(True)
        self.audioInThread.start()

        self.audioOutThread = threading.Thread(target=self.playAudio)
        self.audioOutThread.setDaemon(True)
        self.audioOutThread.start()

    def collectAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.audioInputStream.read(self.CHUNK)
                    self.connect.send(data)
                else:
                    self.connect.shutdown(socket.SHUT_RDWR)
        except Exception as E:
            print(E)
            self.audioInputStream.close()
            return

    def playAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.connect.recv(65536)
                    self.audioOutputStream.write(data)
                else:
                    return
        except Exception:
            self.breakFlag = True
            self.audioOutputStream.close()
            self.pyAU.terminate()
            return

class AUDIOCLIENT:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1

    def __init__(self, IP, port):
        self.audioClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audioClient.connect((IP, port))
        self.pyAU = pyaudio.PyAudio()
        self.audioInputStream = self.pyAU.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          frames_per_buffer=self.CHUNK)
        self.audioOutputStream = self.pyAU.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          output=True,
                                          frames_per_buffer=self.CHUNK)

        self.breakFlag = False

        self.audioInThread = threading.Thread(target=self.collectAudio)
        self.audioInThread.setDaemon(True)
        self.audioInThread.start()

        self.audioOutThread = threading.Thread(target=self.playAudio)
        self.audioOutThread.setDaemon(True)
        self.audioOutThread.start()

    def collectAudio(self):
        try:
                while True:
                    if not self.breakFlag:
                        data = self.audioInputStream.read(self.CHUNK)
                        self.audioClient.send(data)
                    else:
                        self.audioClient.shutdown(socket.SHUT_RDWR)
                        return
        except Exception as E:
            self.audioInputStream.close()
            print(E)
            return

    def playAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.audioClient.recv(65536)
                    self.audioOutputStream.write(data)
                else:
                    return
        except Exception:
            self.breakFlag = True
            self.audioOutputStream.close()
            self.pyAU.terminate()
            return
    