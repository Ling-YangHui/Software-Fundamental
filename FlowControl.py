import threading
import socket
import pyaudio
import wave
import cv2
import numpy as npy

class GETAUDIO():

    def __init__(self):
        self.selfHostIP = "192.168.43.73"
        self.audioPort = 8086
        self.videoPort = 7001
        self.serverAudio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverVideo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audioConnect = None
        self.videoConnect = None
        self.connectionType = "NONE"
        self.connectionCutOff = False

        self.CHUNK  = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100

        self.audioStream = []


    def P2PServerConnect(self):
        self.serverAudio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAudio.bind((self.selfHostIP, self.audioPort))
        self.serverAudio.listen(10)
        self.audioConnect, addr = self.serverAudio.accept()

        self.serverVideo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverVideo.bind((self.selfHostIP, self.videoPort))
        self.serverVideo.listen(10)
        self.videoConnect, addr = self.serverVideo.accept()

        print("RECV!")
        self.connectionType = "SERVER"


    # def P2PClientConnect(self,serverIP, serverPort):
    #     self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.client.self.audioConnect((serverIP, serverPort))
    #     self.connectionType = "CLIENT"


    # def P2PClientDel(self):
    #     self.client.shutdown(socket.SHUT_RDWR)
    #     self.connectionType = "NONE"


    def audioThread(self):
        # newAudioThread.start()
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)
        try:
            while True:
                self.audioStream.clear()
                firstLoop = True
                if self.connectionType == "SERVER" or self.connectionType == "NONE":
                    streamCache = self.audioConnect.recv(65536)
                    stream.write(streamCache)

                # elif self.connectionType == "CLIENT":
                #     for i in range(1, 21):
                #         audioStream.append(self.client.recv(4096))
                #         audioThread = threading.Thread(
                #             target=playAudioThread, args=(audioStream, audioFinished))
                #         audioThread.setDaemon(True)
                #         while (audioFinished[0] == False):
                #             continue

        except Exception as e:
            print(e)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def videoThread(self):
        cv2.namedWindow('VIDEOhost',flags=cv2.WINDOW_AUTOSIZE)
        try:
            videoCache = bytes()
            while True:
                videoCache = b''
                restByteNum = 480 * 640 * 3
                while (restByteNum > 0):
                    videoCache += self.videoConnect.recv(restByteNum)
                    restByteNum -= len(videoCache)
                print(len(videoCache))
                # videoCache = cv2.cvtColor(videoCache,cv2.COLOR_BGR2RGB)
                img = npy.frombuffer(videoCache,npy.uint8)
                try:
                    img.shape = (480,640,3)
                    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                except Exception:
                    continue
                cv2.imshow("VIDEOhost",img)
                if cv2.waitKey(40) & 0xFF == ord('q'):
                    break
                if cv2.waitKey(40) & 0xFF == ord('s'):
                    cv2.waitKey(0)
        except Exception as e:
            print(e)

g = GETAUDIO()
g.P2PServerConnect()

ta = threading.Thread(target=g.audioThread)
ta.setDaemon(True)
ta.start()

tv = threading.Thread(target=g.videoThread)
tv.setDaemon(True)
tv.start()

ta.join()
tv.join()