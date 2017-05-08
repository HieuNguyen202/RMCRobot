// SpeedEncoder.h

#ifndef _SPEEDENCODER_h
#define _SPEEDENCODER_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
	#include "digitalWriteFast.h"
#else
	#include "WProgram.h"
#endif
#include "Timer.h"

class SpeedEncoderClass
{
 protected:
 private:

 public:
	typedef void(*voidFuncPtr)(void); //needed for interuptAttach
	volatile long count1;
	volatile long lastCount1;
	volatile long count2;
	volatile long lastCount2;
	volatile int v1;
	volatile int v2;
	SpeedEncoderClass();
	void attach(voidFuncPtr interuptFunction1, voidFuncPtr interuptFunction2);
	void rise1();
	void rise2();
	void updateSpeed();
	long interval;//mili seconds
	TimerClass timer;
};

extern SpeedEncoderClass SpeedEncoder;

#endif

