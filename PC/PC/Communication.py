# speed ranging from 0 to 127 for stop to full power.
# for Raspberry Pi 3, port = '/dev/serial0' and baudrate = 9600
import time
import binascii
import socket
from Utility import *

class Communication(socket.socket):
    'Communication between two devices using python'
    def __init__(self, host, port, dashboard):
        self.s=socket.socket()
        self.host = host
        self.port = port
        self.connected=False
        self.dashboard=dashboard
        self.speedScale=Scale(-127,127)
        self.prevCommand=-1
        self.prevPrevCommand=-1
    def __str__(self):
        return self.host+":"+str(self.port)

    def connect(self):
        self.dashboard.display("Connecting to ", str(self))
        self.dashboard.disconnected()
        timer1=Timer()
        timer1.resetTimer()
        while self.privateConnect()==False and timer1.timer()<30.0:pass #emmty while loop for 30 seconds 
        if self.connected==False:
            self.dashboard.display("Connection to "+str(self)+" failed.")
        return self.connected
    def privateConnect(self):# to be called by self.connect()
        try:
            self.s.connect((self.host, self.port))
            self.dashboard.display("Connection to "+self.host+":"+str(self.port)+" established.")
            self.dashboard.connected()
            self.connected=True
        except:
            self.connected=False
        finally:
            return self.connected
    def bind(self):
        s.bind(self.host,self.port)
    def send(self, message):
        self.s.send(message)
    def close(self):
        self.s.close()
    def tellPi(self,command, data1, data2=None): # 1 byte message
        if data2==None:#single command
            if data1!=self.prevCommand:
                if command=='left': self.sendInt(int(self.speedScale.unScale(data1,0,63))) 
                elif command=='right': self.sendInt(int(self.speedScale.unScale(data1,64,127)))      
                elif command=='arm': self.sendInt(int(self.speedScale.unScale(data1,127,191)))                    
                elif command=='hand': self.sendInt(int(self.speedScale.unScale(data1,192,255)))    
                self.prevPrevCommand=self.prevCommand
                self.prevCommand=data1              
        else: #double command
            if data1!=self.prevPrevCommand or data2!=self.prevCommand:
                if command=='straight':
                    self.sendInt(int(self.speedScale.unScale(data1,0,63)))
                    self.sendInt(int(self.speedScale.unScale(data2,64,127)))
                elif command=='drive':
                    self.sendInt(int(self.speedScale.unScale(data1,0,63)))
                    self.sendInt(int(self.speedScale.unScale(data2,64,127)))
                elif command=='dig':
                    self.sendInt(int(self.speedScale.unScale(data1,127,191)))
                    self.sendInt(int(self.speedScale.unScale(data2,192,255)))
                self.prevPrevCommand=data1
                self.prevCommand=data2
    def tellPi2(command, data1, data2=None): # 2 byte message
        if data2==None:#single command
            if data1!=self.prevCommand:
                if command=='left': self.sendInt2(int(self.speedScale.unScale(data1,0,255))) 
                elif command=='right': self.sendInt2(int(self.speedScale.unScale(data1,256,511)))      
                elif command=='arm': self.sendInt2(int(self.speedScale.unScale(data1,127,191)))                    
                elif command=='hand': self.sendInt2(int(self.speedScale.unScale(data1,192,255)))    
                self.prevPrevCommand=self.prevCommand
                self.prevCommand=data1              
        else: #double command
            if data1!=self.prevPrevCommand or data2!=self.prevCommand:
                if command=='drive':
                    self.sendInt2(int(self.speedScale.unScale(data1,0,255)))
                    self.sendInt2(int(self.speedScale.unScale(data2,256,511)))
                self.prevPrevCommand=data1
                self.prevCommand=data2
    def sendInt(number): #number from 0 to 255
        hexString=format(number, '02x')#convert int to binary
        message=binascii.hexlify(binascii.unhexlify(hexString))#convert int to binary
        self.send(message)
    def sendInt2(number): #number from 0 to 65535
        hexString=format(number, '04x')#convert int to binary
        message=binascii.hexlify(binascii.unhexlify(hexString))#convert int to binary
        self.send(message)
