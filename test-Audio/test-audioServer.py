from audioCore import AUDIOSERVER

audioServer = AUDIOSERVER('127.0.0.1')
audioServer.startAudio()
audioServer.audioInThread.join()
audioServer.audioOutThread.join()