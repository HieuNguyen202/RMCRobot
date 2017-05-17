import sys
import socket
from Utility import *

serialPort = '/dev/serial0'
baudRate = 9600

def main():
    communication(12346)    
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
    global message
    host =getLocalIP()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)# add this to reuse the port
    s.bind((host,port))
    while True:
        #try:
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
        #except (KeyboardInterrupt, SystemExit):
                print("Keyboard interupted")
                c.close()
                raise
        #except:
            print("Socket comunication failed.")
            c.close()
def run(message):
    if message.getCommandInt()==1:
        print("The robot has been rebooted!")
    else:
        print("In valid command, the only valid command is 1.")
    
if __name__ == "__main__":
        main()

