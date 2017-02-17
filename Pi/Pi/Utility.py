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