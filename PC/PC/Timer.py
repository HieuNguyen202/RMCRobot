import time
class Timer:
    def __init__(self):
        self._timer=time.time()

    def resetTimer(self):
	    self._timer = time.time()

    def timer(self):
	    return time.time()-self._timer

