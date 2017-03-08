#Important notes:
#   Autorun:
#       Rename this file into main.py
#       put it under /home/pi/RMC along with its support files (Ex: Parser.py)
#       Setup auto start using the guide on programming notes
#   Must be ran under Python 3
#2/2/2017
#   Added Parser object: construct and parse commands
#   Added 'run' function: run commands sent from PC
#2/16/2017
#   Added a new communication protocol: send a 1-byte command, whose value ranges from 0 to 255 to represent different function
#   Data usage for the new communication protocol: about 30 bytes/sec (could be reduced even more)
#   Added 'run2' function: to support the new, compressed communication protocol
#   Added 'sDrive' in sabertooth.py
#   Rename sabretooth.py to sabertooth.py
#   Added Ultility.py for small, handy classes
#   Put Timer class in Utility.py

from Sabertooth import *
import time
import socket
import sys
from Utility import *
#if sys.version_info[0]<3: import thread
#else: import _thread

serialPort = '/dev/serial0'
baudRate = 9600
motorAddress=130
actuatorAddress=132
#oneActs=132
wheels = Wheels(serialPort, baudRate, motorAddress)
acts = Wheels(serialPort, baudRate, actuatorAddress)
#hands = Wheels(serialPort, baudRate, oneActs)
#p=Parser("(,)|")# Command analyzer
speedScale=Scale(0,math.pow(2,self.message.numData1Digit)-1,-127,127)
t=Timer()
dataCount=0
#password=123
message=Message()

def main():
    #if sys.version_info[0]<3:thread.start_new_thread(communication,(12345,))
    #else: _thread.start_new_thread(communication,(12345,))
    communication(12345)
def getLocalIP():
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
def communication(port):
    global dataCount
    global message
    host =getLocalIP()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)# add this to reuse the port
    s.bind((host,port))
    while True:
        try:
            numHexPerMessage=message.getLength()/4
            print (str(host)+" is listening for a new connection at port "+str(port))
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
                    message.setValues(eachBlock)
                    run3(message)
                    #codeInt=bin2int()
                    #run(codeInt)
                if t.timer()>60:
                    numBytes=dataCount/2 #1 byte == 2 hex letter
                    print ("Total number of bytes used in 1 minute: ",numBytes)
                    t.resetTimer()
                    dataCount=0
        except:
            print("Socket comunication failed.")
            wheels.stop()
            arms.stop()
            c.close()

def oldrun(input):
    if input[0]=="wheels":
        wheels.drive(input[1],input[2])
    elif input[0]=="left":
        wheels.left(input[1])
    elif input[0]=="arms":
        arms.drive(input[1],input[1])
    elif input[0]=="hands":
        hands.drive(input[1],input[1])
    else:pass
def run(input):
    if input<0: pass
    elif input<64:
        wheels.leftMotor.sDrive(speedScale.scale(input,0,63))
    elif input<128:
        wheels.rightMotor.sDrive(speedScale.scale(input,64,127))
    elif input<192:
        acts.leftMotor.sDrive(speedScale.scale(input,128,191))
    elif input<256:
        acts.rightMotor.sDrive(speedScale.scale(input,192,255))
    else:pass
def run2(input):
    if input<0: pass
    elif input<256:
        wheels.leftMotor.sDrive(speedScale.scale(input,0,255))
    elif input<512:
        wheels.rightMotor.sDrive(speedScale.scale(input,256,511))
    elif input<768:
        acts.leftMotor.sDrive(speedScale.scale(input,512,767))
    else:pass

def run3(message):
    commanInt=self.getCommandInt()
    data1Int=self.getData1Int()
    data2Int=self.getData2Int()
    if commanInt==0:#stop
        wheels.stop()
        arms.stop()
    elif commanInt==1:#drive
        lSpeed=speedScale.scale(message.getData1Int())
        rSpeed=speedScale.scale(message.getData2Int())
        wheels.drive(lSpeed,rSpeed)
    elif commanInt==2:#both
        lSpeed=speedScale.scale(message.getData1Int())
        rSpeed=speedScale.scale(message.getData2Int())
        arms.drive(lSpeed,rSpeed)
    elif commanInt==3:#arm
        speed=speedScale.scale(message.getData1Int())
        arms.leftMotor.sDrive(speed)
    elif commanInt==4:#hand
        speed=speedScale.scale(message.getData1Int())
        arms.rightMotor.sDrive(speed)
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

if __name__ == "__main__":
        main()

