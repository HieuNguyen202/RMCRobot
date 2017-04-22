#To run this, you would need to install two modules: pyserial and pygame
#Need to do:
#   Keep detecting Xbox controller until one is detected
#   Filter duplicated commands
#2/2/2017:
#   Added Speed control for button 4 and 5 down
#   Changed clock tick to 25
#   Added auto reconnect when connect is lost
#   Added Parser class: construct and parse commands
#   Added axis 2 (on the top) control
#   We can alternatively use the right stick as the manual control for the actuator (create a new joystick object, have axis 3 and 4 update XY of the new stick then send an command for the actuators)
#2/16/2017
#   Transfer data in a form of binary to reduce data transmission.
import binascii
import socket
import time
import pygame
import os, sys
import pygame
from Xbox360Controller import *
from Communication import *
from Utility import *
from Dashboard import *

'''There are also some other custom classes whose functions are used by this script, all of them has to be placed in a same folder with this script:
Xbox360Controller: contains the Joystick and Driver class, which tracks joystick coordinate and return scaled motor speed.
Communication: Handle socket communication between a Pi and a PC.
Timer: Just a simple timer like in ECE 100.
Parser: used to construct a command to send to a Pi. It's also used to in a Pi to parse a command back to its elements.
 '''
 #Variables
host = "192.168.2.201" # Destination IP address, Pi's IP address
#host = "192.168.2.110" # Destination IP address, Pi's IP address
commandPort = 12345    # Port that's been opened in the Pi
dashboardSize=(1200,900)

def test():
    dashboard=RMCDashboard(dashboardSize,10,10)


def main():
    dashboard=RMCDashboard(dashboardSize,10,10)
    while True:
        try:
            message=Message(4,6,6)
            commandPipe = Communication(host,commandPort,dashboard,message)
            controller=XboxController(dashboard,commandPipe)
            while True:
                if controller.connected is False:
                    controller.initialize()
                else:
                    if commandPipe.connected is False:
                        commandPipe.connect()
                    else:
                        #test(controller)
                        while True:# consider removing this
                            controller.listen()
        except:
            dashboard.display("Communication or XboxController failed")
            dashboard.disconnected()
            controller.uninitialize()
            dashboard.xboxDisconnected()
            commandPipe.close()
if __name__ == "__main__":
        main()
        #test()