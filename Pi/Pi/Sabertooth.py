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
class Controller(object):
    'A Sabertooth controller'
    def __init__(self, port, baudRate, address):
        self.port = serial.Serial(port, baudRate, timeout=0)
        self.address = address
        self.leftMotor = motor(self.port, address, 1)
        self.rightMotor = motor(self.port, address, 2)
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
        super().__init__(self, port, baudRate, address)

    def left(self,speed):
        self.leftMotor.drive('backward', speed)
        self.rightMotor.drive('forward', speed)
    def right(self,speed):
        self.leftMotor.drive('forward', speed)
        self.rightMotor.drive('backward', speed)
class LinearActuator(Controller):
    'Basic controls for the wheels'
    def __init__(self, port, baudRate, address):
        super().__init__(self, port, baudRate, address)
class motor(object):
    'Serial communication with the Sabertooth.'
    def __init__(self, serial, controllerAddress, motorNum):
        self.port = serial
        self.address = controllerAddress
        self.motorNum = motorNum
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
