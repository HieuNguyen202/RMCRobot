import RPi.GPIO as GPIO
import time
import threading
class Indicator(threading.Thread):
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
    def blink(self):
        self.on()
        time.sleep(0.2)
        self.off()
        time.sleep(0.2)
    def join(self):
        self.status=-1
        super().join()