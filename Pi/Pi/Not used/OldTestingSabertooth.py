#Important notes:
#   Methods put on top, method callers put in bottom
#2/2/2017
#   Added Parser object: construct and parse commands
#   Added 'run' function: run commands sent from PC

from sabretooth import *
from Parser import *
import time
import socket
import sys
import thread

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
                message=str(data)
                commands=p.split(message)#split a big string of commands into small strings of commands
                print (commands)
                for command in commands:
                    run(p.parse(command))#Run a parsed command
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
    else:pass
    
serialPort = '/dev/serial0'
baudRate = 9600
wheels = Wheels(serialPort, baudRate, 130)
p=Parser("(,)|")# Command analyzer
thread.start_new_thread(communication,(12345,))
