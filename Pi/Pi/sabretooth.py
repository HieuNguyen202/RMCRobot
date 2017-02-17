
# speed ranging from 0 to 127 for stop to full power
# for Raspberry Pi 3, port = '/dev/serial0' and baudrate = 9600
import math
import serial
import sys
class Controller(object):
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
#Start Wheels
class Wheels(Controller):
    'Basic controls for the wheels'
    def __init__(self, port, baudRate, address):
        self.port = serial.Serial(port, baudRate, timeout=0)
        self.address = address
        self.leftMotor = motor(self.port, address, 1)
        self.rightMotor = motor(self.port, address, 2)
        
    def left(self,speed):
        self.leftMotor.drive('backward', speed)
        self.rightMotor.drive('forward', speed)
        
    def right(self,speed):
        self.leftMotor.drive('forward', speed)
        self.rightMotor.drive('backward', speed)
#End Wheels
        
#Start LinearActuator
class LinearActuator(Controller):
    'Basic controls for the wheels'
    def __init__(self, port, baudRate, address):
        self.port = serial.Serial(port, baudRate, timeout=0)
        self.address = address
        self.leftMotor = motor(self.port, address, 1)
        self.rightMotor = motor(self.port, address, 2)
#End LinearActuator
    
class motor(object):
    #motorNum is 1 or 2, depending on which motor you wish to control
    def __init__(self, serial, controllerAddress, motorNum):
        self.port = serial
        self.address = controllerAddress
        self.motorNum = motorNum
        if motorNum == 1:
            self.commands = {'forward': 0, 'backward': 1}
        elif motorNum == 2:
            self.commands = {'forward': 4, 'backward': 5}

    def drive(self, direction, speed):
        if speed >127: speed=127
        if speed <0: speed =0
        if sys.version_info[0]<3:
            self.port.write(chr(self.address))
            self.port.write(chr(self.commands[direction]))
            self.port.write(chr(speed))
            self.port.write(chr(int(bin((self.address + self.commands[direction] + speed) & 0b01111111),2)))
        else:
            self.port.write(chr(self.address).encode())
            self.port.write(chr(self.commands[direction]).encode())
            self.port.write(chr(speed).encode())
            self.port.write(chr(int(bin((self.address + self.commands[direction] + speed) & 0b01111111),2)).encode())
