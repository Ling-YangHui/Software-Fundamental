import socket
import threading
import pyaudio


class AudioError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


class AUDIOSERVER:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1

    def __init__(self, IP, clientCore, port):
        self.audioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientCore = clientCore
        self.audioServer.bind((IP, port))
        self.audioServer.listen(16)
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

    def closeAudio(self):
        self.breakFlag = True

    def collectAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.audioInputStream.read(self.CHUNK)
                    self.connect.send(data)
                else:
                    raise AudioError('')
                    return
        except ConnectionResetError:
            self.audioInputStream.close()
            return
        except AudioError:
            self.audioInputStream.close()
            return

    def playAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.connect.recv(65536)
                    self.audioOutputStream.write(data)
                else:
                    raise AudioError('')
                    return
        except ConnectionResetError:
            self.clientCore.messageQueue.put('CallingBreak$')
            self.clientCore.messageEvent.set()
            self.breakFlag = True
            self.audioOutputStream.close()
            self.audioInThread.join()
            self.pyAU.terminate()
            return
        except AudioError:
            self.audioOutputStream.close()
            self.audioInThread.join()
            self.connect.shutdown(socket.SHUT_RDWR)
            self.pyAU.terminate()
            return


class AUDIOCLIENT:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1

    def __init__(self, IP, port, clientCore):
        self.audioClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientCore = clientCore
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

    def closeAudio(self):
        self.breakFlag = True

    def collectAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.audioInputStream.read(self.CHUNK)
                    self.audioClient.send(data)
                else:
                    raise AudioError('')
                    return
        except ConnectionResetError:
            self.audioInputStream.close()
            return
        except AudioError:
            self.audioInputStream.close()
            return

    def playAudio(self):
        try:
            while True:
                if not self.breakFlag:
                    data = self.audioClient.recv(65536)
                    self.audioOutputStream.write(data)
                else:
                    raise AudioError('')
                    return
        except ConnectionResetError:
            self.clientCore.messageQueue.put('CallingBreak$')
            self.clientCore.messageEvent.set()
            self.breakFlag = True
            self.audioOutputStream.close()
            self.audioInThread.join()
            self.pyAU.terminate()
            return
        except AudioError:
            self.audioOutputStream.close()
            self.audioInThread.join()
            self.connect.shutdown(socket.SHUT_RDWR)
            self.pyAU.terminate()
            return
