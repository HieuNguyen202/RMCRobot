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
from HeadlessXbox360Controller import *
from HeadlessCommunication import *
from Utility import *

'''There are also some other custom classes whose functions are used by this script, all of them has to be placed in a same folder with this script:
Xbox360Controller: contains the Joystick and Driver class, which tracks joystick coordinate and return scaled motor speed.
Communication: Handle socket communication between a Pi and a PC.
Timer: Just a simple timer like in ECE 100.
Parser: used to construct a command to send to a Pi. It's also used to in a Pi to parse a command back to its elements.
 '''
 #Variables
#hostLst = ["192.168.2.201", "192.168.2.202","192.168.2.203","192.168.2.204","192.168.2.205"] # List containing the different addresses for the raspberry pi units
host="192.168.2.202"
#i = 0 # counter for the index of the hostLst list. Defaulted to 0.
commandPort = 12345    # Port that's been opened in the Pi

def main():
        print("Target Pi: "+str(host)+":"+str(commandPort))
        while True:
            try:
                message=Message(4,6,6)
                commandPipe = HeadlessCommunication(host,commandPort,message)
                controller=HeadlessXboxController(commandPipe)
                print("Connecting to a Xbox controller...")
                while True:
                    if controller.connected is False:
                        controller.initialize()
                    else:
                        print("Xbox controller connected.")
                        print("Connecting to the robot at "+str(host)+":"+str(commandPort))
                        while True:
                            if commandPipe.connected is False:
                                commandPipe.connect()
                            else:
                                print("Connected to the robot at "+str(host)+":"+str(commandPort))
                                while True:# consider removing this
                                    controller.listen()
            except:
                print("Connection failed!")
                controller.uninitialize()
                commandPipe.close()
if __name__ == "__main__":
        main()