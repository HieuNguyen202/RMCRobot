#Important notes:
#   Autorun:
#       Rename this file into main.py
#       put it under /home/pi/RMC along with its support files (Ex: Parser.py)
#       Setup auto start using the guide on programming notes
#   Methods put on top, method callers put in bottom
#   Running under Python 3
#2/2/2017
#   Added Parser object: construct and parse commands
#   Added 'run' function: run commands sent from PC

from sabretooth import *
from Parser import *
import time
import socket
import sys
from Utility
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
            while True:
                data = c.recv(1024)
                if not data: break
                print(data)
                #run2(bin2int(data))
                #message=str(data)
                #commands=p.split(message)#split a big string of commands into small strings of commands
                #print (commands)
                #for command in commands:
                #    run(p.parse(command))#Run a parsed command
                #print(message)
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
    return int(binary,16)

if __name__ == "__main__":
        main()

