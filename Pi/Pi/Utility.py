import time
import binascii
class Scale(object):
    def __init__(self, inMin,inMax, outMin,outMax):
        self.inMin=inMin
        self.inMax=inMax
        self.outMin=outMin
        self.outMax=outMax
    def scale(self, x):
        return (x - self.inMin) * (self.outMax - self.outMin) / (self.inMax - self.inMin) + self.outMin
class Timer(object):
    def __init__(self):
        self._timer=time.time()

    def resetTimer(self):
	    self._timer = time.time()

    def timer(self):
	    return time.time()-self._timer
class Parser(object):
    'old communication method, works but inefficient'
    def __init__(self,stringFormat):# Ex: "(,)|"
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
        'Split commands out'
        outputList=inputString.split("|")
        outputList=list(filter(None,outputList))
        return outputList

    def parse(self,inputString):# Ex: "(drive,127,1,127,1,0,0)"
        'Parse a command into its elements with correct types'
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
        output=self.leftP
        divider=self.comma
        output+=divider.join(str(e) for e in elements)
        output+=self.rightP+self.bar
        return output
class NumberBase(object):
    'Contains data type conversions necessary for Message object'
    def bin2int(self,bin):
        return int(bin,16)
    def binString2int(self,binString):
        return int(binString,2)
    def bin2binString(self,bin):
        return self.int2binString(self.bin2int(bin),len(bin)*4)#nuber of hex times 4
    def int2bin(self,number,length): #number from 0 to 255
        hexFormat='0'+str(length/4)+'x'
        hexString=format(number, hexFormat)#convert int to binary
        bin=binascii.hexlify(binascii.unhexlify(hexString))#convert int to binary
        return bin
    def int2binString(self,number,size):
        output=bin(number)[2:].zfill(size)
        if len(output)>size:#get the most significant digits if too long
            output=output[:size]
        return output
class Message(NumberBase):
    'Message to be sent to the Pi'
    def __init__(self, numCommandDitgit=None, numData1Digit=None, numData2Digit=None):
        self.numCommandDitgit=None
        self.numData1Digit=None
        self.numData2Digit=None
        self.commandInt=None
        self.data1Int=None
        self.data2Int=None
        if numCommandDitgit is None or numData1Digit is None or numData2Digit is None:
            self.setStructure(2,3,3)
        else: self.setStructure(numCommandDitgit,numData1Digit,numData2Digit)
    def getInt(self): return self.binString2int(self.getBinString())
    def getBin(self): return self.int2bin(self.getInt(),self.getLength()) #return bin data that can be sent by socket
    def getBinString(self): return self.getCommandBinString()+ self.getData1BinString() + self.getData2BinString()
    def getData1Int(self): return self.data1Int
    def getData2Int(self): return self.data2Int
    def getCommandInt(self): return self.commandInt
    def getData1BinString(self): return self.int2binString(self.data1Int,self.numData1Digit)
    def getData2BinString(self): return self.int2binString(self.data2Int,self.numData2Digit)
    def getCommandBinString(self): return self.int2binString(self.commandInt,self.numCommandDitgit)
    def getLength(self):return self.numCommandDitgit+self.numData1Digit+self.numData2Digit
    def setStructure(self,numCommandDitgit, numData1Digit, numData2Digit):
        if isinstance(numCommandDitgit, str): self.numCommandDitgit=self.binString2int(numCommandDitgit)
        else: self.numCommandDitgit=numCommandDitgit
        if isinstance(numData1Digit, str): self.numData1Digit=self.binString2int(numData1Digit)
        else: self.numData1Digit=numData1Digit
        if isinstance(numData2Digit, str): self.data2Int=self.binString2int(numData2Digit)
        else: self.numData2Digit=numData2Digit
    def setValues(self,command,data1=None,data2=None):
        if data1 is None and data2 is None:
            if isinstance(command, str):
                i1=self.numCommandDitgit
                i2=i1+self.numData1Digit
                i3=i2+self.numData2Digit
                self.setValues(command[0:i1],command[i1:i2],command[i2:i3])
            elif isinstance(command, bytes):
                print(command)
                self.setValues(self.bin2binString(command))
        else: 
            if isinstance(command, str): self.commandInt=self.binString2int(command)
            else: self.commandInt=command
            if isinstance(data1, str): self.data1Int=self.binString2int(data1)
            else: self.data1Int=data1
            if isinstance(data2, str): self.data2Int=self.binString2int(data2)
            else: self.data2Int=data2
    def equals(self,that):
        if isinstance(that,Message):
            if self.numCommandDitgit!=that.numCommandDitgit:return False
            if self.numData1Digit!=that.numData1Digit:return False
            if self.numData2Digit!=that.numData2Digit:return False
            if self.commandInt!=that.commandInt:return False
            if self.data1Int!=that.data1Int:return False
            if self.data2Int!=that.data2Int:return False
            return True
        else:
            return False
    
        
  