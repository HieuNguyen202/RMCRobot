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

#if sys.version_info[0]<3: import thread
#else: import _thread

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

t=Timer()
dataCount=0
#password=123
message=Message(4,6,6)
speedScale=Scale(-31,31,-127,127)
#speedScale=Scale(1,math.pow(2,message.numData1Digit)-1,-127,127)

motorAddress = 130
armAddress = 131
handAddress = 132

piController = SabertoothControlers(motorAddress,armAddress,handAddress)
arduinoController = I2C(7)
hybridController = piController

#switches
useArduino=True #use arduino to control the Sabertooths.

def main():
    if  useArduino: tryToConnectArduino();
    
    #if sys.version_info[0]<3:thread.start_new_thread(communication,(12345,))
    #else: _thread.start_new_thread(communication,(12345,))
    communication(12345)
def tryToConnectArduino():
    if  arduinoController.connected():
        arduinoController.setSabertoothAddresses(motorAddress, armAddress, handAddress)
        hybridController = arduinoController
        #tellPC using arduino
    else:
        #tellPC not using arduino
        useArduino=False
def disconnectArduino():
    useArduino=False
    hybridController = piController
    #tellPC not using arduino
        
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
                    run(message)
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
def run1(message):#change to text switch case
    commanInt=message.getCommandInt()
    data1Int=message.getData1Int()
    data2Int=message.getData2Int()
    if commanInt==0:#stop
        hybridController.stopMotor()
        hybridController.stopArm()
        hybridController.stopHand()
    elif commanInt==1:#power drive
        lSpeed=speedScale.scaleInt(data1Int)
        rSpeed=speedScale.scaleInt(data2Int)
        hybridController.setMotorPower(lSpeed,rSpeed)
    elif commanInt==2:#power arm and hand 
        lSpeed=speedScale.scaleInt(data1Int)
        rSpeed=speedScale.scaleInt(data2Int)
        hybridController.setArmPower(lSpeed)
        hybridController.handArmPower(rSpeed)
    elif commanInt==3:#power arm
        speed=speedScale.scaleInt(data1Int)
        hybridController.setArmPower(speed)
    elif commanInt==4:#power hand
        speed=speedScale.scaleInt(data1Int)
        hybridController.handArmPower(speed)
    elif commanInt==5:#speed drive
        lSpeed=speedScale.scaleInt(data1Int)
        rSpeed=speedScale.scaleInt(data2Int)
        hybridController.setMotorSpeed(lSpeed,rSpeed)
    elif commanInt==6:#angular arm and hand 
        armAngle=armAngleScale.scaleInt(data1Int)
        handAngle=handAngleScale.scaleInt(data2Int)
        hybridController.setArmAngle(armAngle)
        hybridController.setHandAngle(handAngle)
    elif commanInt==7:#angular arm
        armAngle=armAngleScale.scaleInt(data1Int)
        hybridController.setArmAngle(armAngle)
    elif commanInt==8:#angular hand
        handAngle=handAngleScale.scaleInt(data1Int)
        hybridController.setHandAngle(handAngle)
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
def i2cTest():
    for x in range(0,18):
        arduinoController.tellArduino(x,[0,1])

if __name__ == "__main__":
        main()

