import time
class Scale(object):
    def __init__(self, min,max):
        self.min = min
        self.max = max

    def scale(self, input,inMin,inMax):
        return (input - inMin) * (self.max - self.min) / (inMax - inMin) + self.min
    def unScale(self, input,inMin,inMax):
        return (input - self.min) * (inMax - inMin) / (self.max - self.min) + inMin
    def setMin(min):
        self.min=min
    def setMax(max):
        self.max=max
    def setExtremes(min,max):
        self.setMin(min)
        self.setMax(max)

class Timer(object):
    def __init__(self):
        self._timer=time.time()

    def resetTimer(self):
	    self._timer = time.time()

    def timer(self):
	    return time.time()-self._timer

class Parser(object):
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
        