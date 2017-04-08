#!/usr/bin/python3

import threading
import time
from Utility import *

class Communication (threading.Thread):
    def __init__(self,name, port, wheels, arms, hands):
        threading.Thread.__init__(self)
        self.name = name
        self.message=None
        self.port = port
        self.wheels = wheels
        self.arms = arms
        self.hands = hands
        self.running=True
    def run(self):
        self.communication()
    def communication(self):
        host =getLocalIP()
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)# add this to reuse the port
        s.bind((host,self.port))
        while self.running:
            try:
                numHexPerMessage=int(self.message.getLength()/4)
                print (str(host)+":"+str(self.port)+" is listening...")
                s.listen(1)
                c, addr = s.accept()
                data = c.recv(1024)
                print("Connection from: "+ str(addr))
                t.resetTimer()
                while True:
                    data = c.recv(1024)
                    if not data: break
                    dataCount=dataCount+len(data)
                    for i in range(0,len(data),numHexPerMessage):
                        eachBlock=data[i:i+numHexPerMessage]
                        self.message.setValues(eachBlock)
                        execute()
            except:
                print("Socket comunication failed.")
                self.wheels.stop()
                self.arms.stop()
                self.hands.stop()
                c.close()
        print("Exiting comunication ", self.name)
        self.wheels.stop()
        self.arms.stop()
        self.hands.stop()
        c.close()
        s.close()
    def execute(self):
        commanInt=self.message.getCommandInt()
        data1Int=self.message.getData1Int()
        data2Int=self.message.getData2Int()
        if commanInt==0:#stop
            self.wheels.stop()
            self.arms.stop()
        elif commanInt==1:#drive
            lSpeed=speedScale.scaleInt(data1Int)
            rSpeed=speedScale.scaleInt(data2Int)
            self.wheels.drive(lSpeed,rSpeed)
        elif commanInt==2:#both
            lSpeed=speedScale.scaleInt(data1Int)
            rSpeed=speedScale.scaleInt(data2Int)
            self.arms.drive(lSpeed,lSpeed)
            self.hands.drive(rSpeed,rSpeed)
        elif commanInt==3:#arm
            self.speed=speedScale.scaleInt(data1Int)
            self.arms.drive(speed,speed)
        elif commanInt==4:#hand
            self.speed=speedScale.scaleInt(data1Int)
            self.hands.drive(speed,speed)
        elif commanInt==5:
            pass
        elif commanInt==6:
            pass
        elif commanInt==7:
            pass
        elif commanInt==8:
            pass
        elif commanInt==9:
            pass
        elif commanInt==10:
            pass
        elif commanInt==11:
            pass
        elif commanInt==12:
            pass
        elif commanInt==13:
            pass
        elif commanInt==14:
            pass
        elif commanInt==15:
            pass
    def getLocalIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP