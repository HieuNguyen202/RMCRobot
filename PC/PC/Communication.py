# speed ranging from 0 to 127 for stop to full power.
# for Raspberry Pi 3, port = '/dev/serial0' and baudrate = 9600
import time
import binascii
import socket
from Timer import *
class Communication(socket.socket):
    'Communication between two devices using python'
    def __init__(self, host, port):
        self.s=socket.socket()
        self.host = host
        self.port = port
        self.connected=False
    def __str__(self):
        return self.host+":"+str(self.port)

    def connect(self,password):
        print("Connecting to ", str(self))
        timer1=Timer()
        timer1.resetTimer()
        while self.privateConnect(password)==False and timer1.timer()<30.0:pass #emmty while loop for 30 seconds 
        if self.connected==False:print("Connection to "+str(self)+" failed.")
        return self.connected

    def privateConnect(self,password):# to be called by self.connect()
        try:
            self.s.connect((self.host, self.port))
            print("Connection to "+self.host+":"+str(self.port)+" established.")
            sendInt(password)
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

    def sendInt(number): #number from 0 to 255
        hexString=format(number, '02x')#convert int to binary
        message=binascii.hexlify(binascii.unhexlify(hexString))#convert int to binary
        self.send(message)

    def sendInt2(number): #number from 0 to 65535
        hexString=format(number, '04x')#convert int to binary
        message=binascii.hexlify(binascii.unhexlify(hexString))#convert int to binary
        self.send(message)