from audioCore import AUDIOCLIENT

audioClient = AUDIOCLIENT('127.0.0.1', 8086)
audioClient.audioInThread.join()
audioClient.audioOutThread.join()