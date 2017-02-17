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
from Parser import *
import time
import socket
import sys
from Utility import *
#if sys.version_info[0]<3: import thread
#else: import _thread

serialPort = '/dev/serial0'
baudRate = 9600
motors=130
twoActs=131
oneActs=132
wheels = Wheels(serialPort, baudRate, motors)
arms = Wheels(serialPort, baudRate, twoActs)
hands = Wheels(serialPort, baudRate, oneActs)
p=Parser("(,)|")# Command analyzer
speedScale=Scale(-127,127)
t=Timer()
dataCount=0

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
    host =getLocalIP()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)# add this to reuse the port
    s.bind((host,port))
    while True:
        try:
            print (str(host)+" is listening for a new connection at port "+str(port))
            s.listen(1)
            c, addr = s.accept()
            print("Connection from: "+ str(addr))
            t.resetTimer()
            while True:
                data = c.recv(1024)
                if not data: break
                dataCount=dataCount+len(data)
                for i in range(0,len(data),2):
                    codeInt=bin2int(data[i:i+2])
                    run2(codeInt)
                #print(data)
                #run2(bin2int(data))
                #message=str(data)
                #commands=p.split(message)#split a big string of commands into small strings of commands
                #print (commands)
                #for command in commands:
                #    run(p.parse(command))#Run a parsed command
                #print(message)
                if t.timer()>60:
                    numBytes=dataCount/2 #1 byte == 2 hex letter
                    print ("Total number of bytes used in 1 minute: ",numBytes)
                    t.resetTimer()
                    dataCount=0
        except:
            print("Socket comunication failed.")
            wheels.stop()
            c.close()
def run(input):
    if input[0]=="wheels":
        wheels.drive(input[1],input[2])
    elif input[0]=="left":
        wheels.left(input[1])
    elif input[0]=="arms":
        arms.drive(input[1],input[1])
    elif input[0]=="hands":
        hands.drive(input[1],input[1])
    else:pass

def run2(input):
    if input<0: pass
    elif input<64:
        wheels.leftMotor.sDrive(speedScale.scale(input,0,63))
    elif input<128:
        wheels.rightMotor.sDrive(speedScale.scale(input,64,127))
    elif input<192:
        arms.leftMotor.sDrive(speedScale.scale(input,128,191))
    elif input<256:
        arms.leftMotor.sDrive(speedScale.scale(input,192,255))
    else:pass

def bin2int(binData):
    return int(binData,16)

if __name__ == "__main__":
        main()

