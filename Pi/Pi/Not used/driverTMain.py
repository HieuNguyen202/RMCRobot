#!/usr/bin/env python
#rafi tether edit 11-25-13
#3-10-14 added load wifi 
#4-4-14 added led indicators
#10-24-15 changing the controls, change the exit button
from time import sleep
from sabretooth import *
import socket
import pygame
import os
from pygame.locals import *

######################################
################################
##
##  ######    ######    ######
## ##    ##  ###       ###
## ##    ##  ##        ##
## ##    ##  ##        ##
## ##    ##  ##        ##
## ##    ##  ###       ###
##  ######    ######    ######
##
################################
######################################

##for tethered, the buttons directly control the motors as opposed to sending it to a different file to read as the wireless

########
### for some reason, all the positive axis do not respond on the motors correctly
### to solve, i set everything to buttons and d pad
########
########   CONTROL LAYOUT ######
### Y & A is arm up/down.  LB & RB is tilt shovel up/down.  Dpad is wheels.
########


##for led autostart notifiers
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#pin numbers
ledwifi = 24  #wifi led
ledteth = 23  #tether led
switch1 = 25
GPIO.setup(ledwifi, GPIO.OUT)
GPIO.setup(ledteth, GPIO.OUT)
GPIO.setup(switch1, GPIO.IN)
#if the script successfully loads, both leds turn on
GPIO.output(ledwifi, True)  
GPIO.output(ledteth, True)
#we're using the term False because we are sinking the current for the Led. So by making it logic LOW,or 0volts, then the led would flow from 3v to gnd to turn on. Why? i dont know if its true for the raspberry pi but on TTL, pins can sink more current than they can source.







##stuff for i2c
import smbus
import time
import subprocess
global irRead
irRead = False
global irSignal
irSignal = 20
global autoSpeed
autoSpeed = 70



bus = smbus.SMBus(1)
address = 0x04
def writeNumber(value):
    try:
        bus.write_byte(address, value)
        # bus.write_byte_data(address, 0, value)
    except IOError:    
        subprocess.call(['i2cdetect','-y','1'])
        errorFlag = 1
        time.sleep(2)
        # Get out the old value
        bus.write_byte(address, value)
    return

def readNumber():
    global number
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

def readIR():
     time.sleep(0.05)
     number = readNumber()
     global irSignal
     irSignal = number
     #return








#############

def main():

        "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
#set up controllers
        serialPort = '/dev/ttyAMA0'
        baudRate = 9600    
        frontCon = controller(serialPort, baudRate, 130)    
        rearCon = controller(serialPort, baudRate, 129)
    #shovel leftMotor will be the arm movement.
    #shovel rightMotor will be the tilt movement
        shovel = controller(serialPort, baudRate, 128)
    
    
        #shovelVert = controller(serialPort, baudRate, 128) old robot
        #shovelTilt = controller(serialPort, baudRate, 135)

        #booston = False
        global quitready
        quitready = False
        global axSpeed
        axSpeed = 90
	global axupSpeed
	axupSpeed = 110
        global whSpeed
	whSpeed = 40
        pygame.init()
        screen = pygame.display.set_mode((40, 40))
        pygame.display.set_caption("JOYTEST")
        clock = pygame.time.Clock()
        joysticks = []
        for i in range(0, pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
                joysticks[-1].init()
                print "Detected joystick '",joysticks[-1].get_name(),"'"
        	#print "Detected joystick '",joysticks[-1].get_name(),"'"
 
### this led code is at this point because if the controller is not plugged in, the script 'crashes' at the
### print "detect" line. so to help us out, i moved the led on line over here.
### if the switch is on, this script is loaded, keeping the tether led on so we know its loaded and turning off the wifi led

        GPIO.output(ledwifi, False) #turns off the wifi led
	while 1:
                clock.tick(60)



                
                
                while (GPIO.input(switch1) == True):
                        #print "starting obstacle avoidance. to quit program use ctrl+C in terminal"
                        irRead = True
                        writeNumber(30)  #idenitfier for IR i2c
                        time.sleep(.2)
                        readIR()  #reads the output of the arduino for the arm.
                        print irSignal
                        
                        if irSignal == 1:
                            print "drive forward"
                            print "The speed magnitude is ", + autoSpeed
                            frontCon.allForward(autoSpeed)
                            rearCon.allForward(autoSpeed)
                        elif irSignal == 2:
                            print "drive backward"
                            print "The speed magnitude is ", + autoSpeed
                            frontCon.allBack(autoSpeed - 5)
                            rearCon.allBack(autoSpeed - 5)
                    
                        elif irSignal == 3:
                            print "drive left"                    
                            frontCon.leftMotor.drive('back', autoSpeed - 10)
                            frontCon.rightMotor.drive('forward', autoSpeed -10)
                            rearCon.leftMotor.drive('back', autoSpeed -10)
                            rearCon.rightMotor.drive('forward', autoSpeed -10)                    
                        elif irSignal == 4:
                            print "drive right"
                            print('executing skid right...')
                            frontCon.leftMotor.drive('forward', autoSpeed -10)            
                            rearCon.leftMotor.drive('forward', autoSpeed -10)
                            frontCon.rightMotor.drive('back', autoSpeed -10)
                            rearCon.rightMotor.drive('back', autoSpeed -10)
                    
                        elif irSignal == 0:
                            print('killing Wheels...')
                            frontCon.allForward(0)
                            rearCon.allForward(0)
                            irRead = False

                        if (GPIO.input(switch1) == False):
                            print('killing Wheels...')
                            frontCon.allForward(0)
                            rearCon.allForward(0)
                            irRead = False
                        
                
                for event in pygame.event.get():
                        if event.type == QUIT:
                                	print "Received event 'Quit', exiting."
                                	return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
                                	print "Escape key pressed, exiting."
					pygame.display.quit()
					sleep(1)
                                	return
########
### for some reason, all the positive axis do not respond on the motors correctly
### to solve, i set everything to buttons and d pad
### Y & A is arm up/down.  LB & RB is tilt up/down.  Dpad is wheels.
                            #### 4-25-14 edit.  move with a,b,x,y. arms and shove is lb,rb,back,start
########
##                        elif event.type == JOYAXISMOTION:
##                                if event.axis == 2:
##                                        if event.value > .3 :
##                                            ## drive forward
##                                            mag = int("%.0f" % abs(event.value * 110))
##                                            print "forward", mag                                          
##                                            frontCon.allForward(int(mag))
##                                            rearCon.allForward(int(mag))					    
##                                        if event.value < -.3 :
##                                            ##drive backward
##                                            print "backward", ("%.3f" % event.value )
##                                            mag = ("%.0f" % abs(event.value * 110))                                            
##                                            frontCon.allBack(int(mag))
##                                            rearCon.allBack(int(mag))
##                                        else:
##                                                frontCon.allForward(0)
##                                                rearCon.allForward(0)
##                                if event.axis == 0:
##                                        if event.value > .5 :
##                                            ## drive right                                              
##                                            print "right", ("%.3f" % event.value )
##                                            mag = ("%.0f" % abs(event.value * 110)) 
##                                            frontCon.leftMotor.drive('forward', int(mag))
##                                            frontCon.rightMotor.drive('back', int(mag))
##                                            rearCon.leftMotor.drive('forward', int(mag))
##                                            rearCon.rightMotor.drive('back', int(mag)) 
##                                        if event.value < -.5 :
##                                            ##drive left
##                                            print "left", ("%.3f" % event.value )
##                                            mag = ("%.0f" % abs(event.value * 110))
##                                            frontCon.leftMotor.drive('back', int(mag))
##                                            frontCon.rightMotor.drive('forward', int(mag))
##                                            rearCon.leftMotor.drive('back', int(mag))
##                                            rearCon.rightMotor.drive('forward', int(mag))
##                                        else:
##                                                frontCon.allForward(0)
##                                                rearCon.allForward(0)
##                                if event.axis == 1:
##                                        if event.value > .7 :
##                                            ## arm down                                         
##                                            print "arm down"
##                                            shovel.allBack(axSpeed)
##                                                
##                                        if event.value < -.7 :
##                                            ## arm up
##                                            print "arm up"
##                                            shovel.allForward(axSpeed)
##                                        else:
##                                                shovel.allForward(0)
##                                                 
##                                if event.axis == 4:
##                                        if event.value > .7 :
##                                            ## tilt down                                                
##                                            print "tilt down"
##                                            shovel.allBack(axSpeed)   
##                                        if event.value < -.7 :
##                                            ## tilt up
##                                            print "tilt up"
##                                            shovel.allForward(axSpeed)
##                                        else:
##                                                shovel.allForward(0)
##                                                shovel.allForward(0)
                        elif event.type == JOYBUTTONUP:
## any up button stops all movement
                                if event.button <= 11:
                                        print "Stopping all movement"                                        
                                        shovel.allForward(0)
		                        frontCon.allForward(0)
                                        rearCon.allForward(0)
                                #print ("Joystick '",joysticks[event.joy].get_name(),
##                                  #  "' button",event.button,"down.")
##                                if event.button == 0:
##                                  	#print "arm down"
##                                      #shovelVert.allBack(axSpeed)
##					#control = "a"           
##                                      #self.btnEvent(control)
##                                if event.button == 1:
##                                    control = "b"
##                                    self.btnEvent(control)
##                                if event.button == 2:
                                     #boost on
                                  ##  print "button x"
##                                if event.button == 3:
##                                    control = "y"
##                                    self.btnEvent(control)
#bumpers make it turn left and right at magnitude of 100
##                                if event.button == 4:   
##                                    #control = "leftbump_down"      #left bumper down 
##                                    #self.btnEvent(control)
##                                    #direction = ""
##                                    direction = "left"                        
##                                    magnitude = 100
##                                    self.joystickEvent(magnitude, direction, 2) 
##                                if event.button == 5:
##                                    #control = "rightbump_down"      #right bumper down
##                                    #self.btnEvent(control)
##                                    #direction = ""
##                                    direction = "right"
##                                    magnitude = 100
##                                    self.joystickEvent(magnitude, direction, 2)                             
##                                if event.button == 6:
##                                    control = "back_down"
##                                    self.btnEvent(control)
##                                if event.button == 7:
##                                    control = "start_down"
##                                    self.btnEvent(control)                                    

                        elif event.type == JOYBUTTONDOWN: 
### the controls say (button)_up because i pasted the code in the up rather than down                           		
###so i just changed it to joybutton down instead of correcting it.
                                #axSpeed = 40
				#global whSpeed
                                #whSpeed = 40

                                ##button 14 and 13 is d pad up and down for wireless controller
##				if event.button == 14:
##					axSpeed -= 10
##					axupSpeed = (axSpeed + 10)
##					print "decreasing actuator speed by 10"
##					if axSpeed == 20:
##						axSpeed = 30
##						axupSpeed = 40
##				if event.button == 13:
##					print "increasing actuator speed by 10:" , axSpeed					
##					axSpeed += 10
##					axupSpeed = (axSpeed + 10)
##					if axSpeed == 130:
##						axSpeed = 120
##						axupSpeed = 120
                                
				if event.button == 10:
					#global whSpeed
                                        ##right thumb stick click in
					print "decreasing speed by 10"
					whSpeed -= 10
					if whSpeed == 10:
						whSpeed = 20
					
				if event.button == 9:
					#global whSpeed
                                        ##left thumb stick click in
					print "increasing speed by 10"
					whSpeed += 10
					if whSpeed == 130:
						whSpeed = 120
					
                              
                                if event.button == 0:
                                        ##axSpeed -= 10
					
					print "decreasing actuator speed by 10"
					if axSpeed == 10:
						axSpeed = 20
						axupSpeed = 30
					axSpeed -= 10
					axupSpeed = (axSpeed + 10)

                                        
                                         

                                    #control = "b_up"
                                    #self.btnEvent(control)
                                if event.button == 1:
                                        print "empty button"
                                    
                                    #control = "a_up"
                                    #self.btnEvent(control)
                                if event.button == 2:
                                    
                                    #boost off
                                    print "x"  
                                if event.button == 3:
                                        ##actualtor increase speed

                                        print "increasing actuator speed by 10:" , axSpeed					
					
					
					if (axSpeed == 120) or (axupSpeed == 120):
						axSpeed = 100
						axupSpeed = 110
					axSpeed += 10
					axupSpeed = (axSpeed + 10)
					

                                if event.button == 4:
                                

                                        
                                    print "tilt down"
                                    shovel.rightMotor.drive('back', axSpeed)
                                    #control = "leftbump_up"     #release to normal
                                    #self.btnEvent(control) 
                                if event.button == 5:
                                    print "tilt up"
                                    shovel.rightMotor.drive('forward', axupSpeed)
                                    #control = "rightbump_up"    #release to normal 
                                    #self.btnEvent(control)
				if event.button == 7:
		    		    print "arm up", axSpeed
                                    shovel.leftMotor.drive('forward', axSpeed) #shovel up 
				if event.button == 6:
		    		    print "arm down", axSpeed
                                    shovel.leftMotor.drive('back', axSpeed) #shovel down 
                                if event.button == 6:
                                    if (quitready == False): quitready = True
                                    else: quitready = False
                                if event.button == 7:
                                    if (quitready):
                                        print "Received event 'Quit', exiting."
					pygame.display.quit()
					sleep(2)
					GPIO.output(ledteth, False)
	            			return
                                        
                        
##				if event.button == 8:
##					##xbox guide button
##		    			
##		    			
                        #print "Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up."
                        elif event.type == JOYHATMOTION:
				  print "dpad"
##                                mag = 70
##                                #print "Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved."
                                  if event.value == (1,0):
				  ## drive right                                              
                                            print " going right" #, ("%.3f" % event.value )
                                            #mag = ("%.0f" % abs(event.value * 110)) 
                                            frontCon.leftMotor.drive('forward', whSpeed)
                                            frontCon.rightMotor.drive('back', whSpeed)
                                            rearCon.leftMotor.drive('forward', whSpeed)
                                            rearCon.rightMotor.drive('back', whSpeed)
                                        
                                  if event.value == (-1,0):
                                        ##drive left
                                            print "left" #, ("%.3f" % event.value )
                                            #mag = ("%.0f" % abs(event.value * 110))
                                            frontCon.leftMotor.drive('back', whSpeed)
                                            frontCon.rightMotor.drive('forward', whSpeed)
                                            rearCon.leftMotor.drive('back', whSpeed)
                                            rearCon.rightMotor.drive('forward', whSpeed)
                                        
                                  if event.value == (0,-1):
                                        print "going backwards", whSpeed                                          
                                        frontCon.allBack(whSpeed)
                                        rearCon.allBack(whSpeed)


                                  if event.value == (0,1):
										
                                        print "forward", whSpeed                                          
                                        frontCon.allForward(whSpeed)
                                        rearCon.allForward(whSpeed)
                                  if event.value == (0,0):
                                  #else:
                                        frontCon.allForward(0)
                                        rearCon.allForward(0)

                
if __name__ == "__main__":

##this stalls the load up for a couple seconds just to correct a seen error where the script
##still sees the switch as off rather than on.
    for x in range(0,5):
        sleep(1)
    if GPIO.input(switch1) == False: ## is the switch is closed, start the program. if off, then it quits.
        print ("switch is on. you are in tethered mode.")
	main()
    else:  ##if switch is off(opened), load wireless
        print "open wireless mode on pc"
##disabled auto load wireless because we would not have feedback about the raspberry.
##so load putty, and start driverMain.py then you will have feedback
        #os.system('sudo python lunabot/driverMain.py')  #while this opens the other script, it appears as if this file stays open in like a "paused" mode.
        #print "exiting wireless mode"  #then once the other file closed, then it resumes here and ends the program here
        GPIO.output(ledteth, False) #now both led's will be off
        print "closing tethered program"	
        #return                       
