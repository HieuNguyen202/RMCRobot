# speed ranging from 0 to 127 for stop to full power.
# for Raspberry Pi 3, port = '/dev/serial0' and baudrate = 9600
import time
import binascii
import socket
import math
from Utility import *

class HeadlessCommunication(socket.socket):
    'Communication between two devices using python'
    def __init__(self, host, port, message):
        super().__init__()
        self.message=message
        self.host = host
        self.port = port
        self.connected=False
        #self.speedScale=Scale(-127,127,1,math.pow(2,self.message.numData1Digit)-1)
        self.speedScale=Scale(-127,127,-31,31)
        self.prevMessageInt=-1
        self.commandDict={'stop':0,'drive':1, 'dig':2,'arm':3,'hand':4}

    def __str__(self): return self.host+":"+str(self.port)
    def connect(self):
        timer1=Timer()
        timer1.resetTimer()
        while self.privateConnect()==False and timer1.timer()<30.0:pass #emmty while loop for 30 seconds 
        return self.connected
    def privateConnect(self):# to be called by self.connect()
        try:
            
            super().settimeout(1)
            super().connect((self.host, self.port))
            #super().settimeout(None)
            self.connected=True
        except:
            self.connected=False
        finally:
            return self.connected
    def bind(self): super().bind(self.host,self.port)
    def tellPi(self, rawCommand, rawData1=None, rawData2=None): # 2 byte message   
        commandInt=self.commandDict[rawCommand]
        if commandInt==0:
            data1Int=0
            data2Int=0
        elif commandInt==1:
            data1Int=self.speedScale.scaleInt(rawData1)
            data2Int=self.speedScale.scaleInt(rawData2)
        elif commandInt==2:
            data1Int=self.speedScale.scaleInt(rawData1)
            data2Int=self.speedScale.scaleInt(rawData2)
        elif commandInt==3:
            data1Int=self.speedScale.scaleInt(rawData1)
            data2Int=0
        elif commandInt==4:
            data1Int=self.speedScale.scaleInt(rawData1)
            data2Int=0
        self.message.setValues(commandInt,data1Int,data2Int)
        thisMessageInt=self.message.getInt()
        if thisMessageInt != self.prevMessageInt: 
            self.send(self.message.getBin())
            self.prevMessageInt=thisMessageInt