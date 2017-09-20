import time
import binascii
#import RPi.GPIO as GPIO
import threading
class Scale(object):
    '''Scale a number from one scale to another (Ex: 2 in (0:10) scale is equivalent to 20 in (0:100) scale)'''
    def __init__(self, inMin,inMax, outMin,outMax):
        self.inMin=inMin
        self.inMax=inMax
        self.outMin=outMin
        self.outMax=outMax
    def scale(self, x):
        return (x - self.inMin) * (self.outMax - self.outMin) / (self.inMax - self.inMin) + self.outMin
    def scaleInt(self,x):
        return int(self.scale(x))
    def __str__(self, **kwargs):
        return "inMin: " + str(self.inMin) +" inMax: " + str(self.inMax)+" outMin: " + str(self.outMin)+" outMax: " + str(self.outMax)
class Timer(object):
    '''As its name suggests, it's a timmer!'''
    def __init__(self): self._timer=time.time()
    def resetTimer(self): self._timer = time.time()
    def timer(self): return time.time()-self._timer
class Parser(object):
    def __init__(self,stringFormat=None):# Ex: "(,)|"
        '''This is rather a ineffective way of communicating with the Rasberry Pi.
        It constructs a string of letters such as (drive,127,1,127,1,0,0)|
        That string then will be asscii encoded and sent to the Raspberry Pi (by a Communication object).
        In terms of size, each message costs about 20 bytes in content + 20 bytes in tcp header = 40 bytes in total.
        This classes was not used in the competition, but we still left it here for learning purposes.
        '''
        if stringFormat==None: stringFormat="(,)|"
        dividers=tuple(stringFormat)
        self.leftP=dividers[0]
        self.comma=dividers[1]
        self.rightP=dividers[2]
        self.bar=dividers[3]
    def paint(self,data,dataType):# return data with valid type
        if int(dataType)==1: return int(data)
        elif int(dataType)==2: return float(data)
        else:return str(data)
    def split(self,inputString):
        'Cut a string of many commands into a list of single commands'
        outputList=inputString.split("|")
        outputList=list(filter(None,outputList))
        return outputList
    def parse(self,inputString):# Ex: "(drive,127,1,127,1,0,0)"
        'INPUT a command string such as (drive,127,1,127,1,0,0) RETURN a list of its elements'
        inputString=inputString.replace(self.leftP,"")
        inputString=inputString.replace(self.rightP,"")
        e=inputString.split(self.comma) # elements
        output=[]
        output.append(str(e[0]))
        for i in range(1,len(e)-1):
            if i%2==1:   
                output.append(self.paint(e[i],e[i+1]))
        return output #Ex:list (drive,127,127,0)
    def construct(self,elements):
        'The opposite of parse: INPUT a list of elements, RETURN a string of combined elements'
        output=self.leftP
        divider=self.comma
        output+=divider.join(str(e) for e in elements)
        output+=self.rightP+self.bar
        return output
class NumberBase(object):
    '''A part of a more efficient way to send messages to the Raspberry Pi
    This is a base class that handles all data conversion for the Message class.
    Notes for data types in this class:
        int: Human friendly representation (Ex: 0 means stop, 1 means drive the motor)
        binString: More of a coded representation. It is a string of 1's and 0's (Ex: "1001", notice this is still a string so it's 4 bytes)
        bin: This is what a socket object would be able to send via the network. (Notice this is real binary, so 1001 or 00001001 is 1 byte) 
    '''
    def bin2int(self,bin): return int(bin,16)
    def binString2int(self,binString): return int(binString,2)
    def bin2binString(self,bin): return self.int2binString(self.bin2int(bin),len(bin)*4)#nuber of hex times 4
    def int2bin(self,number,length): #number from 0 to 255
        hexFormat='0'+str(int(length/4))+'x' # Ex: '02x' for 2-digit hex, '04x' for 4-digit hex
        hexString=format(number, hexFormat)
        bin=binascii.hexlify(binascii.unhexlify(hexString))
        return bin
    def int2binString(self,number,size):
        output=bin(number)[2:].zfill(size) #fill the most significant bits with zeros
        if len(output)>size: #get the most significant digits if the number is too long
            output=output[:size]
        return output
class Message(NumberBase):
    '''A more efficient way of sending commands to the Raspberry Pi.
    Each command/message contains three elements: the command type, data1 and data2.
    For example, command = 1, data1 = 127, data2 = 127 means drive the motors at full speed forward.
    However, 1, 127 and 127 are packed into a 2-byte binary number, so it doesn't use up a lot of bandwidth.
    Let's say we had a message of structrure 4, 6, 6 (meaning 4 bits of command, 6 bits of data1, and 6 bits of data2).
    The binary representation of that message (drive the motors at full speed forward) would be 0001 111111 111111 (1 63 63 in decimal)
    Notice a 6-bit binary can represent 64 different things (0 to 63), but we need 255 differnt representation for the motor speed (-127 to 127),
    so we accepted to lose the speed resolution and scaled the value of data1 and data2 from (0 to 63) scale to (-127 to 127) scale.
    This way, 111111 in bin or 63 in decimal means the max speed 127 for the motor (There is a Scale class up on the top of this file will handle the scaling)
    Advantages: 1) use less bandwidth, each message costs only 2 bytes in the message + 20 bytes in the TCP header = 22 bytes; therefore, faster robot performance.
                2) can tell the robot to do 2^16 = 65535 different things with only 2-byte messages.
    Later on, we scaled the motor speed in (-127:127) scale to (1:63) scale before sending the message
              When the message arrives at the Raspberry Pi, the speed would be anti-scaled back to (-127:127).
              We chose (1:63) instead of (0:63) in order to match the 0 in (-127:127) scale with a whole number in the other scale (i.e. (1:63))
    '''
    def __init__(self, numCommandDitgit=None, numData1Digit=None, numData2Digit=None):
        self.numCommandDitgit=None
        self.numData1Digit=None
        self.numData2Digit=None
        self.commandInt=-1
        self.data1Int=-1
        self.data2Int=-1
        if numCommandDitgit is None or numData1Digit is None or numData2Digit is None:
            self.setStructure(2,3,3)
        else: self.setStructure(numCommandDitgit,numData1Digit,numData2Digit)
    def getInt(self): return self.binString2int(self.getBinString()) #integer representation of the whole message, meaningless but can be converted to bin
    def getBin(self): return self.int2bin(self.getInt(),self.getLength()) #binary representation of the whole message, again meaningless but it is something a socket object would send
    def getBinString(self): return self.getCommandBinString()+ self.getData1BinString() + self.getData2BinString() #representation the whole message as a string of 1's and 0's
    def getData1Int(self): return self.data1Int-31 #value of data1 as an int
    def getData2Int(self): return self.data2Int-31
    def getCommandInt(self): return self.commandInt 
    def getData1BinString(self): return self.int2binString(self.data1Int,self.numData1Digit) #value of data1 in binString representation
    def getData2BinString(self): return self.int2binString(self.data2Int,self.numData2Digit)
    def getCommandBinString(self): return self.int2binString(self.commandInt,self.numCommandDitgit)
    def getLength(self):return self.numCommandDitgit+self.numData1Digit+self.numData2Digit #bitwise length of the whole message
    def setStructure(self,numCommandDitgit, numData1Digit, numData2Digit): #Ex: setStructure(4,6,6) means use 4 bits, 6 bits for data1 and 6 bits for data2. ccccddddddDDDDDD
        if isinstance(numCommandDitgit, str): self.numCommandDitgit=self.binString2int(numCommandDitgit) # input could be in binString form (Ex: '101')
        else: self.numCommandDitgit=numCommandDitgit # or in integer form (Ex: 5)
        if isinstance(numData1Digit, str): self.numData1Digit=self.binString2int(numData1Digit)
        else: self.numData1Digit=numData1Digit
        if isinstance(numData2Digit, str): self.data2Int=self.binString2int(numData2Digit)
        else: self.numData2Digit=numData2Digit
    def setValues(self,command,data1=None,data2=None):
        'Set values (command, data1, data2)for a new message'
        if data1 is None and data2 is None: #command variable contains info of all (command, data1 and data2)
            if isinstance(command, str): #overloaded command variable could be a binString
                i1=self.numCommandDitgit
                i2=i1+self.numData1Digit
                i3=i2+self.numData2Digit
                self.setValues(command[0:i1],command[i1:i2],command[i2:i3])
            elif isinstance(command, bytes): #or a bin
                self.setValues(self.bin2binString(command))
        else: #command variable contains only info the command, other info is held by their own variable names.
            if isinstance(command, str): self.commandInt=self.binString2int(command) #binString
            else: self.commandInt=command #bin
            if isinstance(data1, str): self.data1Int=self.binString2int(data1)
            else: self.data1Int=data1+31
            if isinstance(data2, str): self.data2Int=self.binString2int(data2)
            else: self.data2Int=data2+31
    def __eq__(self, that): #not tested
        'Test if 2 instances of a Message are the same'
        if isinstance(that,Message):
            if self.numCommandDitgit!=that.numCommandDitgit:return False
            if self.numData1Digit!=that.numData1Digit:return False
            if self.numData2Digit!=that.numData2Digit:return False
            if self.commandInt!=that.commandInt:return False
            if self.data1Int!=that.data1Int:return False
            if self.data2Int!=that.data2Int:return False
            return True
        else: return False
    def __str__(self, **kwargs):
        return "int: "+str(self.getInt())+" bin: "+str(self.getBinString())+" commandInt: "+str(self.getCommandInt())+" data1Int: "+str(self.getData1Int())+" data2Int: "+str(self.getData2Int())
class Indicator(threading.Thread):
    '''LED indications of the state of the robot. This object can be multithreaded, so it won't interfere robot's performance'''
    def __init__(self, pinNum):
        threading.Thread.__init__(self)
        self.pinNum = pinNum
        self.status=0 #0 for off, 1 for on, 2 for blink
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pinNum,GPIO.OUT)
    
    def run(self):
        while self.status>-1:
            if self.status==0:
                self.off()
            elif self.status==1:
                self.on()
            elif self.status==2:
                self.blink()
        self.off()
    def on(self):
        GPIO.output(self.pinNum,GPIO.HIGH)
    def off(self):
        GPIO.output(self.pinNum,GPIO.LOW)
    def bilnk(self):
        self.on()
        time.sleep(0.2)
        self.off()
        time.sleep(0.2)
    def join(self):
        self.status=-1
        super().join()