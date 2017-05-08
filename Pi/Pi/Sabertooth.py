'''
This file contains classes that control a Sabertooth.
Each Controller object has two motor objects.
A Motor object contains functions that send serial signal to the Sabertooth to drive the motors.
Wheels is a another kind of Controller.Besides having everything a Controller has,
Wheels also has some additional functions that are more specific to the wheels.
Similarly, LinearActuator is also another kind of Controller with some additional functions.
'''

# speed ranging from 0 to 127 for stop to full power (if not specified)
# for Raspberry Pi 3, port = '/dev/serial0' and baudrate = 9600.
import math
import serial
import sys
class SabertoothControlers(object):
    """A Sabertooth controller"""
    def __init__(self, motorAddress, armAddress, handAddress):
        self.serialPort = '/dev/serial0'
        self.baudRate = 9600
        self.DEDAULT_MOTOR_ADDRESS = 130
        self.DEDAULT_ARM_ADDRESS = 131
        self.DEDAULT_HAND_ADDRESS = 132

        #speedFactors is only for the right motor (the slower one)
        self.speedFactors={-81:0.972,
                      -102:0.97,
                      -122:0.975,
                      81:0.970,
                      102:0.975,
                      122:0.997,
                      }
        setMotorAddress(motorAddress)
        setArmAddress(armAddress)
        setHandAddress(handAddress)
    def setMotorAddress(self, address):
        if address<128 or address>135: address=self.DEDAULT_MOTOR_ADDRESS
        self.wheels = Wheels(self.serialPort, self.baudRate, address)
    def setArmAddress(self, address):
        if address<128 or address>135: address=self.DEDAULT_ARM_ADDRESS
        self.arms = LinearActuator(self.serialPort, self.baudRate, address, self.speedFactors)
    def setHandAddress(self, address):
        if address<128 or address>135: address=self.DEDAULT_HAND_ADDRESS
        self.hands = LinearActuator(self.serialPort, self.baudRate, address)
    def setMotorPower(self, lPower, rPower):
        """Sets power for the left and right motors.
           param lPower level for the left motor. Integers from -127 to 127.       
           param rPower level for the right motor. Integers from -127 to 127."""
        self.wheels.drive(lPower,rPower)
    def setArmPower(self, power):
        """Sets power for the actuators of the arm.
           param power the same power level for both actuators of the arm. Integers from -127 to 127."""
        self.arms.drive(power)
    def setHandPower(self, power):
        """Sets power for the actuator of the hand.
           param power level for the actuator of the hand. Integers from -127 to 127."""
        self.hands.drive(power)
        def setArmHeight(self, height):
        """Set the height of the shovel. Take y value when arm angle is zero to be to 0 reference of height.
           param target shovel height in centimeters. Could be negative or possitive. 0 for horizontal position.        
           """
        self.tellArduino(self.i2cCommands['set_arm_height_offset'], height + self.heightOffset)
    def setArmAngle(self, angle):
        """Set robot arm angle. Take the angle value when arm angle is horizontal to be to 0 reference.
           param target shovel angle in degrees. Could be negative or possitive. 0 for horizontal position."""
        pass
    def setHeightOffset(self, offset):
        """Sets offset for the height of the shovel
           param offset the offset of the height in centimeters"""
        pass
    def setAngleOffset(self, offset):
        """Sets offset for the angle of the arm
           param offset the offset of the angle in degrees."""
        pass
    def setMotorSpeed(self, lSpeed, rSpeed):
        """Sets speed for the left and right motors.
           param lSpeed speed level for the left motor (pulses/miliseconds)       
           param rSpeed speed level for the right motor (pulses/miliseconds)     
           note that the speed levels are offsetted by +xxx here, so make sure the
           Arduino program offsets them by -xxx to bright them back to their original values."""
        pass
    def setHandHeightOffset(self, offset):
        """Sets offset for the height of the tip of the shovel
           param offset the offset of the height in centimeters."""
        pass
    def setHandHeight(self, height):
        """Set the height ofthe tip of the shovel. Take y value when arm angle is zero to be to 0 reference of height.
           param height target height of the tip of the shovel in centimeters. Could be negative or possitive. 0 for horizontal position."""
        pass
    def setHandAngle(self, angle):
        """Set robot hand angle. Take the angle value when hand angle is horizontal to be to 0 reference.
           param angle target shovel angle in degrees. Could be negative or possitive. 0 for horizontal position."""
        pass
    def setHandAngleOffset(self, offset):
        """Sets offset for the angle of the hand
           param offset the offset of the angle in degrees
           """
        pass
    def stopMotor(self):
        """Stop motor power."""
        self.setMotorPower(0,0)
    def stopArm(self):
        """Stop arm power."""
        self.setArmPower(0,0)
    def stopHand(self):
        """Stop hand power."""
        self.setHandPower(0,0)
class Controller(object):
    """A Sabertooth controller"""
    def __init__(self, port, baudRate, address, speedFactors=None): #speedFactors is only for the right motor (the faster one)
        self.port = serial.Serial(port, baudRate, timeout=0)
        self.address = address
        self.leftMotor = motor(self.port, address, 1) #M1 is left, M2 is right
        self.rightMotor = motor(self.port, address, 2, speedFactors)
    def forward(self, speed):
        self.leftMotor.drive('forward', speed)
        self.rightMotor.drive('forward', speed)
    def backward(self, speed):
        self.leftMotor.drive('backward', speed)
        self.rightMotor.drive('backward', speed)
    def stop(self):
        self.leftMotor.drive('forward', 0)
        self.rightMotor.drive('forward', 0)
    def drive(self,leftSpeed,rightSpeed):#speed ranging from -127 to 127 this this particular function
        if leftSpeed<0:
            self.leftMotor.drive('backward', int(math.fabs(leftSpeed)))
        else:
            self.leftMotor.drive('forward', int(math.fabs(leftSpeed)))
        if rightSpeed<0:
            self.rightMotor.drive('backward',int( math.fabs(rightSpeed)))
        else:
            self.rightMotor.drive('forward', int(math.fabs(rightSpeed)))
class Wheels(Controller):
    'Basic controls for the wheels'
    def __init__(self, port, baudRate, address):
        super().__init__(port, baudRate, address)
    def left(self,speed):
        self.leftMotor.drive('backward', speed)
        self.rightMotor.drive('forward', speed)
    def right(self,speed):
        self.leftMotor.drive('forward', speed)
        self.rightMotor.drive('backward', speed)
class LinearActuator(Controller):
    'Basic controls for the wheels'
    def __init__(self, port, baudRate, address, speedFactors=None ):
        super().__init__(port, baudRate, address, speedFactors )
    def drive(self, speed):
        super().drive(speed, speed)
class motor(object):
    'Serial communication with the Sabertooth.'
    def __init__(self, serial, controllerAddress, motorNum, speedFactors=None):
        #tel = {'jack': 4098, 'sape': 4139}
        self.port = serial
        self.address = controllerAddress
        self.motorNum = motorNum
        if speedFactors==None: self.speedFactors=dict()
        else: self.speedFactors =speedFactors
        if motorNum == 1:
            self.commands = {'forward': 0, 'backward': 1}
        elif motorNum == 2:
            self.commands = {'forward': 4, 'backward': 5}
    def sDrive(self, speed):# Smart drive! It knows negative speed backward, so speed could range is from -127 to 127
        if speed<0:
            self.drive('backward',int(math.fabs(speed)))
        else:
            self.drive('forward',int(math.fabs(speed)))
    def drive(self, direction, speed):#Dumb drive! Has no idea about negative numbers. Speed range is from 0 to 127
        speedFactor=1
        if direction=="forward":
            if speed in self.speedFactors: speedFactor=self.speedFactors[speed]                
        else: 
            if -speed in self.speedFactors: speedFactor=self.speedFactors[-speed] 
        speed=speed*speedFactor #reduce speed the make actuators synced
        if speed >127: speed=127
        if speed <0: speed =0
        speed=int(speed)
        if sys.version_info[0]<3: #Python 2
            self.port.write(chr(self.address))
            self.port.write(chr(self.commands[direction]))
            self.port.write(chr(speed))
            self.port.write(chr(int(bin((self.address + self.commands[direction] + speed) & 0b01111111),2)))
        else: #Python 3
            self.port.write(chr(self.address).encode())
            self.port.write(chr(self.commands[direction]).encode())
            self.port.write(chr(speed).encode())
            self.port.write(chr(int(bin((self.address + self.commands[direction] + speed) & 0b01111111),2)).encode())
