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
#3/11/2017
#   Added Indicator class
#   Write a i2c receiver in Arduino
#   Add system commends to PC and Pi
from Sabertooth import *
import time
import socket
import sys
from Utility import *

serialPort = '/dev/serial0'
baudRate = 9600
#speedFactors is only for the right motor (the slower one)
speedFactors={-81:0.972,
              -102:0.97,
              -122:0.975,
              81:0.970,
              102:0.975,
              122:0.997,
              }
sabertoothAddress={0: 128,
                        1: 129,
                        2: 130,
                        3: 131,
                        4: 132,
                        5: 133,
                        6: 134,
                        7: 135,}
wheels = Wheels(serialPort, baudRate, 130)
arms = LinearActuator(serialPort, baudRate, 131,speedFactors)
hands = LinearActuator(serialPort, baudRate, 132)

message=Message(4,6,6)
speedScale=Scale(1,math.pow(2,message.numData1Digit)-1,-127,127)

def main():
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
            numHexPerMessage=int(message.getLength()/4)
            print (str(host)+":"+str(port)+" is listening...")
            s.listen(1)
            c, addr = s.accept()
            print("Connection from: "+ str(addr))
            data = c.recv(1024)
            while True:
                data = c.recv(1024)
                if not data: break
                for i in range(0,len(data),numHexPerMessage):
                    eachBlock=data[i:i+numHexPerMessage]
                    message.setValues(eachBlock)
                    run(message)
        except:
            print("Socket comunication failed.")
            wheels.stop()
            arms.stop()
            hands.stop()
            c.close()
def run(message):
    commanInt=message.getCommandInt()
    data1Int=message.getData1Int()
    data2Int=message.getData2Int()
    if commanInt==0:#stop
        wheels.stop()
        arms.stop()
    elif commanInt==1:#drive
        lSpeed=speedScale.scaleInt(data1Int)
        rSpeed=speedScale.scaleInt(data2Int)
        wheels.drive(lSpeed,rSpeed)
    elif commanInt==2:#both
        lSpeed=speedScale.scaleInt(data1Int)
        rSpeed=speedScale.scaleInt(data2Int)
        arms.drive(lSpeed)
        hands.drive(rSpeed)
    elif commanInt==3:#arm
        speed=speedScale.scaleInt(data1Int)
        arms.drive(speed)
    elif commanInt==4:#hand
        speed=speedScale.scaleInt(data1Int)
        hands.drive(speed)
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

