#!/usr/bin/python3
import math
class Joystick:
   'Xbox360 Joystick control. This class keeps track of the joystick coordinate and returns a set of left and right motor speed based on the coordinate of the stick in a XY plane'
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
           print("Spin right ", speed)
           return speed
       elif math.fabs(angle)>180-self.SPINNING_ANGLE:# spin left region
           speed =(int(-speedFactor*fullSpeed),int(speedFactor*fullSpeed))
           if mode!=0:
                speed=(0,speed[1])
           print("Spin left ", speed)
           return speed
       elif angle<0: #backward region
           angle=math.fabs(angle)
           if angle<=90-self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,self.SPINNING_ANGLE,90-self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed = (int(-speedFactor*fullSpeed),int(-speedFactor*fullSpeed*curveFactor))
               print("Backward right", speed)
               return speed
               
           if angle>=90+self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,180-self.SPINNING_ANGLE,90+self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed = (int(-speedFactor*fullSpeed*curveFactor),int(-speedFactor*fullSpeed))
               print("Backward left", speed)
               return speed
               
           else:
               speed =(int(-speedFactor*fullSpeed),int(-speedFactor*fullSpeed))
               if mode!=0:
                    speed=(speed[0],0)
               print("Backward straight", speed)
               return speed
               
       else: #forward reason
           if angle<=90-self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,self.SPINNING_ANGLE,90-self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed =(int(speedFactor*fullSpeed),int(speedFactor*fullSpeed*curveFactor))
               if mode!=0:
                   speed=(speed[0],speed[0])
               print("forward right", speed)
               return speed
               
           if angle>=90+self.EQUAL_SPEED_ANGLE:
               curveFactor=self.map(angle,180-self.SPINNING_ANGLE,90+self.EQUAL_SPEED_ANGLE,self.CURVE_FACTOR,1)
               speed = (int(speedFactor*fullSpeed*curveFactor),int(speedFactor*fullSpeed))
               if mode!=0:
                   speed=(speed[1],speed[1])
               print("forward left", speed)
               return speed
               
           else:
               speed =(int(speedFactor*fullSpeed),int(speedFactor*fullSpeed))
               if mode!=0:
                    speed=(speed[0],0)
               print("forward straight", speed)
               return speed

class Driver(Joystick):
    'a class to handle joystick coordinate and convert it to motor speeds: parametter: (maxSpeeds, indexOfInitialMaxSpeed)'
    def __init__(self,maxSpeeds,initalSpeedIndex):
        self.x = 0.0
        self.y = 0.0
        self.maxSpeeds=maxSpeeds
        self.currentSpeed=self.maxSpeeds[initalSpeedIndex]
    def speedUp(self): # Switch to speed of the next index in maxSpeeds, if is last index, currentSpeed stay the same.
        i=self.maxSpeeds.index(self.currentSpeed)
        if i<len(self.maxSpeeds)-1:
            i=i+1
            self.currentSpeed=self.maxSpeeds[i]
    def slowDown(self): # Switch to speed of the previous index in maxSpeeds, if is 0 index, currentSpeed stay the same.
        i=self.maxSpeeds.index(self.currentSpeed)
        if i>0:
            i=i-1
            self.currentSpeed=self.maxSpeeds[i]
    def speeds(self,mode): # return speeds of left and right motors based on stick coordinate.
        return self.getSpeed(self.currentSpeed,mode)
                

          

