#!/usr/bin/python3
import math
import pygame
import sys
from pygame.locals import *
from pygame.key import *
from Utility import *
#from Parser import *
from Dashboard import *
from Communication import *

class Joystick:
   'Convert joystick coordinate to Sabertooth-readable numbers. For example, (1,1) to (127, 127)'
   stickCount = 0
   SPINNING_ANGLE=20 #angle in degrees from the positive and negative x axis in which spinning operation is executed
   CURVE_FACTOR=0.0 #lowest percentage of fullspeed, which determine the speed of the slower motor when the robot is turning. 1 will have two motor running at the same speed.
   EQUAL_SPEED_ANGLE = 10 #angle in degrees from the positive and negative y axis in which the speed of 2 motors are always the same
   ZERO_EQUIVALANCE=0.3 #less than this mean zero

   def __init__(self,SPINNING_ANGLE=None,CURVE_FACTOR=None,EQUAL_SPEED_ANGLE=None,ZERO_EQUIVALANCE=None):
      self.x = 0.0
      self.y = 0.0

      #Joystick.stickCount += 1
   #def __str__(self):
      #return 'Point (%f, %f)' % (self.x, self.y)

   def setX(self, x):
       self.x = x
       if x>1.0:
           self.x=1.0
       elif x<-1.0:
           self.x=-1.0

   def setY(self, y):
       self.y = y
       if y>1.0:
           self.y=1.0
       elif y<-1.0:
           self.y=-1.0

   def setXY(self, x,y):
       setX(x)
       setY(y)

   def getX(self):
       return self.x

   def getY(self):
       return self.y

   def getXY(self):
       return (self.x,self.y)

   def distToOrigin(self):
       dist =math.sqrt(math.pow(self.x,2)+math.pow(self.y,2))
       if dist>1.0:
           dist=1.0
       return dist

   def map( self, input, in_min, in_max, out_min, out_max): #Scale a number from one scale to another. Ex: 5 in (0 to 10) scale is equivalent to 50 in (0 to 100) scale
	   output = (input - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	   return output

   def getSpeed(self,fullSpeed,mode):# TA DEVIDE BY 0: mode = 0 for wheels; mode=1 for actuators
       speedFactor=self.distToOrigin() #The perentage of the motor speed with respect to max speed, measured by distance to origin of the joystick coordinate
       if speedFactor<self.ZERO_EQUIVALANCE: speedFactor=0 # if the joy stick is 0.3 away from its center, consider it as the center
       speed=(0,0)
       angle = math.degrees(math.atan2(self.y,self.x)) #angle in degrees from the possitive x axis, angle is possitive at I and II quadrants, negative at III and IV quadrants
       if math.fabs(angle)<self.SPINNING_ANGLE:#spin right region
           speed =(int(speedFactor*fullSpeed),int(-speedFactor*fullSpeed))
           if mode!=0:
               speed=(0,speed[1])
           #print("Spin right ", speed)
           return speed
       elif math.fabs(angle)>180-self.SPINNING_ANGLE:# spin left region
           speed =(int(-speedFactor*fullSpeed),int(speedFactor*fullSpeed))
           if mode!=0:
                speed=(0,speed[1])
           #print("Spin left ", speed)
           return speed
       elif angle<0: #backward region
           angle=math.fabs(angle)
           if angle<=90-self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,self.SPINNING_ANGLE,90-self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed = (int(-speedFactor*fullSpeed),int(-speedFactor*fullSpeed*curveFactor))
               #print("Backward right", speed)
               return speed
               
           if angle>=90+self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,180-self.SPINNING_ANGLE,90+self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed = (int(-speedFactor*fullSpeed*curveFactor),int(-speedFactor*fullSpeed))
               #print("Backward left", speed)
               return speed
               
           else:
               speed =(int(-speedFactor*fullSpeed),int(-speedFactor*fullSpeed))
               if mode!=0:
                    speed=(speed[0],0)
               #print("Backward straight", speed)
               return speed
               
       else: #forward reason
           if angle<=90-self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,self.SPINNING_ANGLE,90-self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed =(int(speedFactor*fullSpeed),int(speedFactor*fullSpeed*curveFactor))
               if mode!=0:
                   speed=(speed[0],speed[0])
               #print("forward right", speed)
               return speed
               
           if angle>=90+self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,180-self.SPINNING_ANGLE,90+self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed = (int(speedFactor*fullSpeed*curveFactor),int(speedFactor*fullSpeed))
               if mode!=0:
                   speed=(speed[1],speed[1])
               #print("forward left", speed)
               return speed
               
           else:
               speed =(int(speedFactor*fullSpeed),int(speedFactor*fullSpeed))
               if mode!=0:
                    speed=(speed[0],0)
               #print("forward straight", speed)
               return speed

class JoystickDriver(Joystick):
    'A child of Joystick, Handle max speeds.'
    def __init__(self,maxSpeeds,initalSpeedIndex):
        self.x = 0.0
        self.y = 0.0
        self.maxSpeeds=maxSpeeds
        self.currentMaxSpeed=self.maxSpeeds[initalSpeedIndex]
    def speedUp(self): # Switch to speed of the next index in maxSpeeds, if is last index, currentMaxSpeed stay the same.
        i=self.maxSpeeds.index(self.currentMaxSpeed)
        if i<len(self.maxSpeeds)-1:
            i=i+1
            self.currentMaxSpeed=self.maxSpeeds[i]
        return i
    def slowDown(self): # Switch to speed of the previous index in maxSpeeds, if is 0 index, currentMaxSpeed stay the same.
        i=self.maxSpeeds.index(self.currentMaxSpeed)
        if i>0:
            i=i-1
            self.currentMaxSpeed=self.maxSpeeds[i]
        return i
    def speeds(self,mode): # return speeds of left and right motors based on stick coordinate.
        return self.getSpeed(self.currentMaxSpeed,mode)

class XboxController(object):
    'a class to handle joystick coordinate and convert it to motor speeds: parametter: (maxSpeeds, indexOfInitialMaxSpeed)'
    def __init__(self,dashboard,commandPipe):
        pygame.init()
        self.connected=False
        self.dashboard=dashboard
        self.clock = pygame.time.Clock() # control the xbox controller's frequency of updating button and joystick events.
        self.joysticks = []
        self.wheels=JoystickDriver((50,100,127),1) #a class to handle joystick coordinate and convert it to motor speeds: parametter: (maxSpeeds, indexOfInitialMaxSpeed)
        self.arms=JoystickDriver((50,100,127),1) #a class to handle joystick coordinate and convert it to motor speeds: parametter: (maxSpeeds, indexOfInitialMaxSpeed)
        self.arms.SPINNING_ANGLE=25
        self.arms.EQUAL_SPEED_ANGLE=25
        self.triggerAbs=0 # Moving forward and backward using top triggers has higher priority than the using the stick. This is to ensure the sticks won't take over control if top triggers are being used.
        self.AXIS_2_ZERO_EQUIVALENT=0.1 # if top triggers' value is less than this number, it's considered zero.
        self.JOYSTICK_ZERO_EQUIVALENT=0.2
        self.commandPipe=commandPipe
        self.clockTick=40
        #self.clock.tick(self.clockTick) # 25 is good, how frequently the pygame module updates xbox events. Ex: 25 means 25 times/sec
        
        
    def listen(self):
        'Listen to xbox key events and call the corresponding functions if an button is pressed or a joystick is moved.'
        for event in pygame.event.get():
            if event.type==QUIT: self.quit(event)
            elif event.type == KEYDOWN and event.key == K_ESCAPE: self.quit(event)
            elif event.type == KEYDOWN: keyDownevent(event)
                        #elif event.type == MOUSEMOTION:
                #       print "Mouse movement detected."
            elif event.type == KEYUP: keyUp(event)
            elif event.type == MOUSEBUTTONDOWN: self.mouseButtonDown(event)
            elif event.type == MOUSEBUTTONUP: self.mouseButtonUp(event)
            elif event.type == JOYAXISMOTION: self.joyAxisMotion(event)
            elif event.type == JOYBUTTONDOWN: self.joyButtonDown(event)           
            elif event.type == JOYBUTTONUP: self.joyButtonUp(event)
            elif event.type == JOYHATMOTION: self.joyHatMotion(event)           
    def joyAxisMotion(self,event):
        'This function update X and Y coordinate of the joysticks, converts it into speeds (from -127 to 127), send the command to the Pi.'
        self.clock.tick(self.clockTick)
        if (event.axis==0): #left stick, horizontal
            self.wheels.setX(event.value)
        elif (event.axis==1): #left stick, vertical
            if self.triggerAbs<self.AXIS_2_ZERO_EQUIVALENT: #if using the top triggers, don't update Y
                self.wheels.setY(-event.value)

        elif (event.axis==4):#right stick, vertical.
            self.arms.setX(event.value)
        elif (event.axis==3):#right stick, horizontal
            if self.triggerAbs<self.AXIS_2_ZERO_EQUIVALENT: #if using the top triggers, don't update Y
                self.arms.setY(-event.value)

        elif (event.axis==2):
            self.wheels.setY(-event.value)#Update the value of top triggers to Y, right trigger for going forward, left trigger for going backward.
            self.triggerAbs=math.fabs(event.value) #Update this so next time, it knows whether top triggers are being used.
        else:pass

        if (event.axis==0 or event.axis==1 or event.axis==2):
            speeds=self.wheels.speeds(0) #Get valid Sabertooth speed based on XY coordinate of the joysticks. Ex: (-127,100)
            self.commandPipe.tellPi('drive',speeds[0],speeds[1])
        elif(event.axis==3 or event.axis==4):
            speeds=self.arms.speeds(1) #Get valid Sabertooth speed based on XY coordinate of the joysticks. Ex: (-127,100)
            self.commandPipe.tellPi('dig',speeds[0],speeds[1])
    def keyDown(self,event):
        'Keyboard events, this is how you hack ones password'
        print ("Keydown,",event.key)
    def keyUp(self,event):
        'Keyboard events'
        print ("Keyup,",event.key)
    def mouseButtonDown(self,event):
        'Mouse button'
        #print ("Mouse button",event.button,"down at",pygame.mouse.get_pos())
        pass
    def mouseButtonUp(self,event):
        "Mouse button"
        #print ("Mouse button",event.button,"up at",pygame.mouse.get_pos())
        pass
    def joyButtonDown(self,event):
        'A=0, B=1, X=2, Y=3, LB=4, RB=5, BACK=6, START=7, LEFT JOY BUTTON=8, RIGHT JOY BUTTON=9 down'
        if event.button==0: #A Lowers the arm
            self.commandPipe.tellPi('arm',-(self.arms.currentMaxSpeed-7))
        if event.button==3: #Y Raises the arm
            self.commandPipe.tellPi('arm',(self.arms.currentMaxSpeed-7))
        if event.button==5: #RB Increase max speed of self.wheels or arms
            if self.arms.distToOrigin()>self.JOYSTICK_ZERO_EQUIVALENT: self.dashboard.arm(self.arms.speedUp()+1) #if the right joytick if off center more than the left one, change arm speed. Change wheel speed otherwise
            else: self.dashboard.motor(self.wheels.speedUp()+1)
        if event.button==4: #LB decrease max speed of wheel or arms
            if self.arms.distToOrigin()>self.JOYSTICK_ZERO_EQUIVALENT: self.dashboard.arm(self.arms.slowDown()+1) #if the right joytick if off center more than the left one, change arm speed. Change wheel speed otherwise
            else: self.dashboard.motor(self.wheels.slowDown()+1)
        if event.button==6:
            self.dashboard.arm(self.arms.slowDown()+1) # decrease max speed of arms
        if event.button==7:
            self.dashboard.arm(self.arms.speedUp()+1) # increase max speed of arms
        if event.button==2: #Increase max speed of self.wheels or arms (Change later depending on the feel of the robot)
            self.commandPipe.tellPi('hand',-(self.arms.currentMaxSpeed-7))
        if event.button==1: #Increase max speed of self.wheels or arms
            self.commandPipe.tellPi('hand',(self.arms.currentMaxSpeed-7))
        #print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"down.")
        print ("Wheel speed: ",self.wheels.currentMaxSpeed,"     -     Arms speed: ", self.arms.currentMaxSpeed)
    def joyButtonUp(self,event):
        'A=0, B=1, X=2, Y=3, LB=4, RB=5, BACK=6, START=7, LEFT JOY BUTTON=8, RIGHT JOY BUTTON=9 up'
        #print ("Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up.")
        #print ("Joystick button",event.button,"up.")
        if event.button==0: self.commandPipe.tellPi('arm',0)
        if event.button==3: self.commandPipe.tellPi('arm',0)
        if event.button==2: self.commandPipe.tellPi('hand',0)
        if event.button==1: self.commandPipe.tellPi('hand',0)
    def joyHatMotion(self,event):
        '''Up, down left right buttons next to the right joystick. Could be used for actuator manual control. Its value is like points in a unit circle:
        left=(-1,0) - right=(1,0) - up=(0,1) - down=(0,-1) - upleft=(-1,1) - upright=(1,1) - downleft=(-1,-1) - downright(1,-1) - not pressed=(0,0)'''
        #print ("Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved: ",event.value)
        if event.value == (1,0): #right
            self.commandPipe.tellPi('hand',-(self.arms.currentMaxSpeed-7))
            self.commandPipe.tellPi('arm',0)
        elif event.value == (-1,0): #left
            self.commandPipe.tellPi('hand',(self.arms.currentMaxSpeed-7))
            self.commandPipe.tellPi('arm',0)
        elif event.value == (0,-1): #down
            self.commandPipe.tellPi('hand',0)
            self.commandPipe.tellPi('arm',-(self.arms.currentMaxSpeed-7))
        elif event.value == (0,1): #up
            self.commandPipe.tellPi('hand',0)
            self.commandPipe.tellPi('arm',(self.arms.currentMaxSpeed-7))
        elif event.value == (1,1): #upright
            self.commandPipe.tellPi('hand',-(self.arms.currentMaxSpeed-7))
            self.commandPipe.tellPi('arm',(self.arms.currentMaxSpeed-7))
        elif event.value == (-1,1): #upleft
            self.commandPipe.tellPi('hand',(self.arms.currentMaxSpeed-7))
            self.commandPipe.tellPi('arm',(self.arms.currentMaxSpeed-7))
        elif event.value == (-1,-1): #downleft
            self.commandPipe.tellPi('hand',(self.arms.currentMaxSpeed-7))
            self.commandPipe.tellPi('arm',-(self.arms.currentMaxSpeed-7))
        elif event.value == (1,-1): #downright
            self.commandPipe.tellPi('hand',-(self.arms.currentMaxSpeed-7))
            self.commandPipe.tellPi('arm',-(self.arms.currentMaxSpeed-7))
        elif event.value == (0,0): #not pressed
            self.commandPipe.tellPi('hand',0)
            self.commandPipe.tellPi('arm',0)
    def quit(self,event):
        self.dashboard.display("Exiting...")
        pygame.display.quit()
        sys.exit()
    def initialize(self):
        'Detect if a XboxController is connected. If there is, initialize it.'
        self.dashboard.display("Looking for a Xbox Controller...")
        pygame.joystick.quit()
        pygame.joystick.init()
        t1=Timer()
        t1.resetTimer()
        numJoysticks=pygame.joystick.get_count();

        while numJoysticks==0 and t1.timer()<30:
            pygame.joystick.quit()
            pygame.joystick.init()
            numJoysticks=pygame.joystick.get_count();

        if numJoysticks>0:
            for i in range(0, numJoysticks):
                    self.joysticks.append(pygame.joystick.Joystick(i))
                    self.joysticks[-1].init() #Initialize the one that was just appended
            self.connected=True
            self.dashboard.display("Found a Xbox Controller.")
            self.dashboard.display("Clock tick:  "+str(self.clockTick))
            self.dashboard.xboxConnected()
        else:
            self.connected=False
            self.dashboard.display("Could not find a Xbox Controller.")
            self.dashboard.xboxDisconnected()
    def uninitialize(self):
        'Detect if a XboxController is connected. If there is, initialize it.'
        pygame.joystick.quit()
        self.dashboard.display("Released xbox controllers.")