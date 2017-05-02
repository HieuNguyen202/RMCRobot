// Pot.h

#ifndef _POT_h
#define _POT_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class PotClass
{
 protected:
	 int getRawValue();

	 

 public:
	PotClass(int potPin);
	PotClass();
	void init(int potPin);
	int getValue();
	float getAngle();
	void setMax();
	void setMin();
	void setMaxAngle(float newAngle);
	void setMinAngle(float newAngle);
	void setFactor();
	float raw2Angle(int raw);
	int angle2Raw(float angle);
	float mapfloat(float x, float in_min, float in_max, float out_min, float out_max);
	String toString();
	int potPin;    // select the input pin for the potentiometer
	int max;
	int min;
	float maxAngle;
	float minAngle;
	float factor; // pot reading/ degree

};

extern PotClass Pot;

#endif

