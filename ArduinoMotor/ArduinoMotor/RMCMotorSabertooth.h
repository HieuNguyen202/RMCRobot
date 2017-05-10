// RMCMotorSabertooth.h

#ifndef _RMCMOTORSABERTOOTH_h
#define _RMCMOTORSABERTOOTH_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
#include "RMCSabertooth.h"
#include "Timer.h"

class RMCMotorSabertoothClass:public RMCSabertoothClass
{
 protected:


 public:
	 RMCMotorSabertoothClass();
	 RMCMotorSabertoothClass(byte address, byte initialMode, int speedUpdatePeriod);
	 void init(int speedUpdatePeriod);
	 void setMotorPower(int lPower, int rPower);
	 void setMotorSpeed(int lSpeed, int rSpeed);
	 void Update();
	 int leftTargetSpeed; //for speed control
	 int rightTargetSpeed;
	 int lPower; //for power control
	 int rPower;
	 TimerClass speedTimer;
	 int speedUpdatePeriod; //mili seconds
	 const int DEFAULT_UPDATE_PERIOD = 20;
};

extern RMCMotorSabertoothClass RMCMotorSabertooth;

#endif

