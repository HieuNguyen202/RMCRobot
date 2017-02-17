#To run this, you would need to install two modules: pyserial and pygame
#Need to do:
#   Keep detecting Xbox controller until one is detected
#   Transfer data in a form of binary to reduce data transmission.
#2/2/2017:
#   Added Speed control for button 4 and 5 down
#   Changed clock tick to 25
#   Added auto reconnect when connect is lost
#   Added Parser class: construct and parse commands
#   Added axis 2 (on the top) control
#   We can alternatively use the right stick as the manual control for the actuator (create a new joystick object, have axis 3 and 4 update XY of the new stick then send an command for the actuators)
import binascii
import socket
import time
import _thread
import pygame
import os, sys
import pygame
from pygame.locals import *
from pygame.key import *
from Xbox360Controller import *
from Communication import *
from Timer import *
from Parser import *
from Utility import *

'''There are also some other custom classes whose functions are used by this script, all of them has to be placed in a same folder with this script:
Xbox360Controller: contains the Joystick and Driver class, which tracks joystick coordinate and return scaled motor speed.
Communication: Handle socket communication between a Pi and a PC.
Timer: Just a simple timer like in ECE 100.
Parser: used to construct a command to send to a Pi. It's also used to in a Pi to parse a command back to its elements.
 '''
 #Variables
pygame.init()
joysticks = [] #this is for detectJoysticks function
clock = pygame.time.Clock() # control the xbox controller's frequency of updating button and joystick events.

wheels=Driver((50,100,127),1) #a class to handle joystick coordinate and convert it to motor speeds: parametter: (maxSpeeds, indexOfInitialMaxSpeed)
arms=Driver((50,100,127),1) #a class to handle joystick coordinate and convert it to motor speeds: parametter: (maxSpeeds, indexOfInitialMaxSpeed)
arms.SPINNING_ANGLE=25
arms.EQUAL_SPEED_ANGLE=25

host = "192.168.2.201" # Destination IP address, Pi's IP address
commandPort = 12345    # Port that's been opened in the Pi
feedbackPort=12346     # Open this port on local computer to listen to feedbac from the pi if needed.
#feedbackPipe = Communication(host,feedbackPort) #Not needed
#_thread.start_new_thread(startListening,(feedbackPipe,))  
commandPipe = Communication(host,commandPort)  

triggerAbs=0 # Moving forward and backward using top triggers has higher priority than the using the stick. This is to ensure the sticks won't take over control if top triggers are being used.
leftStickDist=0 # current distance to the center of the left joystick
rightStickDist=0 # current distance to the center of the right joystick
AXIS_2_ZERO_EQUIVALENT=0.1 # if top triggers' value is less than this number, it's considered zero.
JOYSTICK_ZERO_EQUIVALENT=AXIS_2_ZERO_EQUIVALENT
speedScale=Scale(-127,127)
p=Parser("(,)|") #This object is to construct and parse commands. Ex: (drive, 127,2,127,2,0,0)|
def test():
    global speedScale
    for i in range(-128,128):
        print(i," to ",int(speedScale.unScale(i,64,127)))
def main():
    global commandPipe
    #loadDashboard() #loading gaming window.
    detectJoysticks() #detect a joy stick
    #test()
    while True:                                                     #connect to Pi and start sniffing xbox events
        try:
            commandPipe = Communication(host,commandPort)           #Create a socket object
            while commandPipe.connect()==False: pass                #Try connecting until connected
            while True:
                sniffKeys()                                         #Loop to read xbox events, send commands to Pi untill socket communication fails
        except:
            print("Socket communication or sniffKeys function failed")
            commandPipe.close()
  
def startListening(pipe):
    'Listen to feedback from a Pi, but not needed for now. Put this under a multithreading process'
    pipe.bind()
    while True:
        try:
            pipe.listen(1)
            c, addr = pipe.accept()
            print("Connection from: "+ str(addr))
            while True:
                data = c.recv(1024)
                if not data: break
                message=data.decode("ascii")
                print(message)
        except:
            print(str(pipe)+" failed, waiting for new a new connection.")
            c.close()
def loadDashboard():
    screen=pygame.display.set_mode((640,480),0,24)
    pygame.display.set_caption('Monkey Fever')
    #a=100
    #screen.fill((255,255,255))
    #if pygame.key.get_focused():
    #    press=pygame.key.get_pressed()
    #    for i in range(0,len(press)): 
    #        if press[i]==1:
    #            name=pygame.key.name(i)
    #            text=f1.render(name,True,(0,0,0))
    #            screen.blit(text,(100,a))
    #            a=a+100
    #pygame.display.update()
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    f1=pygame.font.SysFont("comicsansms",24)                        
    background = background.convert()
    background.fill((250, 250, 250))
def detectJoysticks():
    'Detect if a joystick is connected. If there is, initialize it.'
    t1=Timer()
    numJoysticks=pygame.joystick.get_count();
    print("Dectecting a joystick...")
    t1.resetTimer()
    while numJoysticks==0 and t1.timer()<30.:#Search for a joystick for 30 seconds
        numJoysticks=pygame.joystick.get_count();
    if numJoysticks>0:
        for i in range(0, numJoysticks):
                joysticks.append(pygame.joystick.Joystick(i))
                joysticks[-1].init()
                print ("Detected joystick '",joysticks[-1].get_name(),"'")
                _thread.start_new_thread(sniffKeys,())
        return True
    else: return False
def sniffKeys():
    'Listen to xbox key events and call the corresponding functions if an button is pressed or a joystick is moved.'
    clock.tick(25)# 25 is good, how frequently the pygame module updates xbox events. Ex: 25 means 25 times/sec
    for event in pygame.event.get():
        if event.type==QUIT: quit(event)
        elif event.type == KEYDOWN and event.key == K_ESCAPE: quit(event)
        elif event.type == KEYDOWN: keyDownevent(event)
                    #elif event.type == MOUSEMOTION:
            #       print "Mouse movement detected."
        elif event.type == KEYUP: keyUp(event)
        elif event.type == MOUSEBUTTONDOWN: mouseButtonDown(event)
        elif event.type == MOUSEBUTTONUP: mouseButtonUp(event)
        elif event.type == JOYAXISMOTION: joyAxisMotion(event)
        elif event.type == JOYBUTTONDOWN: joyButtonDown(event)           
        elif event.type == JOYBUTTONUP: joyButtonUp(event)
        elif event.type == JOYHATMOTION: joyHatMotion(event)           

#Functions to be called by sniffKeys
def joyAxisMotion(event):
    'This function update X and Y coordinate of the joysticks, converts it into speeds (from -127 to 127), send the command to the Pi.'
    global triggerAbs    #label this global so this function knows "triggerAbs" been created somewhere else, don't make a new "triggerAbs" here.
    global leftStickDist
    global rightStickDist
    message=""
    if (event.axis==0): #left stick, horizontal
        wheels.setX(event.value)
        leftStickDist=wheels.distToOrigin()
    elif (event.axis==1): #left stick, vertical
        if triggerAbs<AXIS_2_ZERO_EQUIVALENT: #if using the top triggers, don't update Y
            wheels.setY(-event.value)
            leftStickDist=wheels.distToOrigin()

    elif (event.axis==4):#right stick, vertical.
        arms.setX(event.value)
        rightStickDist=arms.distToOrigin()
    elif (event.axis==3):#right stick, horizontal
        if triggerAbs<AXIS_2_ZERO_EQUIVALENT: #if using the top triggers, don't update Y
            arms.setY(-event.value)
            rightStickDist=arms.distToOrigin()

    elif (event.axis==2):
        wheels.setY(-event.value)#Update the value of top triggers to Y, right trigger for going forward, left trigger for going backward.
        triggerAbs=math.fabs(event.value) #Update this so next time, it knows whether top triggers are being used.
        leftStickDist=wheels.distToOrigin()
    else:pass

    if (event.axis==0 or event.axis==1 or event.axis==2):
        speeds=wheels.speeds(0) #Get valid Sabertooth speed based on XY coordinate of the joysticks. Ex: (-127,100)
        tellPi('drive',speeds[0],speeds[1])
        #message= p.construct(("wheels",speeds[0],2,speeds[1],2)) #Construct a drive command to be sent to the Pi.
    elif(event.axis==3 or event.axis==4):
        speeds=arms.speeds(1) #Get valid Sabertooth speed based on XY coordinate of the joysticks. Ex: (-127,100)
        tellPi('dig',speeds[0],speeds[1])
        #message= p.construct(("arms",speeds[0],2,speeds[1],2)) #Construct a drive command to be sent to the Pi.
    #send(message)
    #print(message)

def keyDown(event):
    'Keyboard events, this is how you hack ones password'
    print ("Keydown,",event.key)
def keyUp(event):
    'Keyboard events'
    print ("Keyup,",event.key)
def mouseButtonDown(event):
    'Mouse button'
    print ("Mouse button",event.button,"down at",pygame.mouse.get_pos())
def mouseButtonUp(event):
    "Mouse button"
    print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())
def joyButtonDown(event):
    'A=0, B=1, X=2, Y=3, LB=4, RB=5, BACK=6, START=7, LEFT JOY BUTTON=8, RIGHT JOY BUTTON=9 down'
    if event.button==0: #A Lowers the arm
        tellPi('hand',-80)
        #message= p.construct(("arms",-80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    if event.button==3: #Y Raises the arm
        tellPi('arm',80)
        #message= p.construct(("arms",80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    if event.button==5: #RB Increase max speed of wheels or arms
        if arms.distToOrigin()>JOYSTICK_ZERO_EQUIVALENT: arms.speedUp() #if the right joytick if off center more than the left one, change arm speed. Change wheel speed otherwise
        else: wheels.speedUp()
    if event.button==4: #LB decrease max speed of wheel or arms
        if arms.distToOrigin()>JOYSTICK_ZERO_EQUIVALENT: arms.slowDown() #if the right joytick if off center more than the left one, change arm speed. Change wheel speed otherwise
        else: wheels.slowDown()
    if event.button==2: #Increase max speed of wheels or arms (Change later depending on the feel of the robot)
        tellPi('hand',-80)
        #message= p.construct(("hands",-80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    if event.button==1: #Increase max speed of wheels or arms
        tellPi('hand',80)
        #message= p.construct(("hands",80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    #print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"down.")
    print ("Wheel speed: ",wheels.currentSpeed,"     -     Arms speed: ", arms.currentSpeed)
def joyButtonUp(event):
    'A=0, B=1, X=2, Y=3, LB=4, RB=5, BACK=6, START=7, LEFT JOY BUTTON=8, RIGHT JOY BUTTON=9 up'
    if event.button==0: #Increase max speed of wheels or arms
        tellPi('arm',0)
        #message= p.construct(("arms",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    if event.button==3: #Increase max speed of wheels or arms
        tellPi('arm',0)
        #message= p.construct(("arms",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    if event.button==2: #Increase max speed of wheels or arms
        tellPi('hand',0)
        #message= p.construct(("hands",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    if event.button==1: #Increase max speed of wheels or arms
        tellPi('hand',0)
        #message= p.construct(("hands",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
    #print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up.")
    print ("Joystick button",event.button,"up.")
def joyHatMotion(event):
    '''Up, down left right buttons next to the right joystick. Could be used for actuator manual control. Its value is like points in a unit circle:
    left=(-1,0) - right=(1,0) - up=(0,1) - down=(0,-1) - upleft=(-1,1) - upright=(1,1) - downleft=(-1,-1) - downright(1,-1) - not pressed=(0,0)'''
    if event.value == (1,0): #right
        tellPi('hand',-80)
        tellPi('arm',0)
        #message= p.construct(("hands",-80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",0,2))
        #send(message)
    elif event.value == (-1,0):
        tellPi('hand',80)
        tellPi('arm',0)
        #message= p.construct(("hands",80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",0,2))
        #send(message)
    elif event.value == (0,-1):
        tellPi('hand',0)
        tellPi('arm',-80)
        #message= p.construct(("hands",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",-80,2))
        #send(message)
    elif event.value == (0,1):
        tellPi('hand',0)
        tellPi('arm',80)
        #message= p.construct(("hands",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",80,2))
        #send(message)
    elif event.value == (1,1):
        tellPi('hand',-80)
        tellPi('arm',80)
        #message= p.construct(("hands",-80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",80,2))
        #send(message)
    elif event.value == (-1,1):
        tellPi('hand',80)
        tellPi('arm',80)
        #message= p.construct(("hands",80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",80,2))
        #send(message)
    elif event.value == (-1,-1):
        tellPi('hand',80)
        tellPi('arm',-80)
        #message= p.construct(("hands",80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",-80,2))
        #send(message)
    elif event.value == (1,-1):
        tellPi('hand',-80)
        tellPi('arm',-80)
        #message= p.construct(("hands",-80,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",-80,2))
        #send(message)
    elif event.value == (0,0):
        tellPi('hand',0)
        tellPi('arm',0)
        #message= p.construct(("hands",0,2)) #Construct a drive command to be sent to the Pi.
        #send(message)
        #message= p.construct(("arms",0,2))
        #send(message)

    print ("Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved: ",event.value)
def quit(event):
    print ("Received event 'Quit', exiting.")
    pygame.display.quit()
def send(message):
    'receives a message as a String, encodes it to ASCII before sending it to the Pi'
    commandPipe.send(message.encode('ascii'))

def tellPi(command, data1, data2=None):
    if command=='left':
        sendInt(int(speedScale.unScale(data1,0,63)))
    elif command=='right':
        sendInt(int(speedScale.unScale(data1,64,127)))
    elif command=='arm':
        sendInt(int(speedScale.unScale(data1,127,191)))
    elif command=='hand':
        sendInt(int(speedScale.unScale(data1,192,255)))
    elif command=='straight':
        sendInt(int(speedScale.unScale(data1,0,63)))
        sendInt(int(speedScale.unScale(data1,64,127)))
    elif command=='drive':
        sendInt(int(speedScale.unScale(data1,0,63)))
        sendInt(int(speedScale.unScale(data2,64,127)))
    elif command=='dig':
        sendInt(int(speedScale.unScale(data1,127,191)))
        sendInt(int(speedScale.unScale(data2,192,255)))
    if data2 is not None:
        print(command," ",data1," ", data2)
    else: print(command," ",data1)
    
def sendInt(number): #number from 0 to 255
    hexString=format(number, '02x')#convert int to binary
    message=binascii.hexlify(binascii.unhexlify(hexString))#convert int to binary
    commandPipe.send(message)

if __name__ == "__main__":
        main()