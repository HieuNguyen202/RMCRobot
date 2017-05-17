from HeadlessCommunication import *
from Utility import *
import sys
import time

'''This program will try to connect to a remote restart Pi in the robot. Once the connectin is established, the remote restart pi in the robot will
restart the main pi of the robot. '''
 #Variables
host="192.168.2.205"
commandPort = 12346    # Port that's been opened in the Pi

def main():
        print("Target Pi: "+str(host)+":"+str(commandPort))
        try:
            message=Message(4,6,6)
            commandPipe = HeadlessCommunication(host,commandPort,message)
            print("RMC Remote Restart: Connecting to "+str(host)+":"+str(commandPort))
            while not commandPipe.connected:
                commandPipe.connect()
            print("Success!")
            commandPipe.close()
        except (KeyboardInterrupt, SystemExit):
            print("Keyboard interupted")
            commandPipe.close()
            raise
        except:
            print("Failed, program exited!")
            commandPipe.close()
if __name__ == "__main__":
        main()