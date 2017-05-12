//!  PID Class. 
/*!
This is class is written for the IIT's mining robot who competes in NASA Robotic Mining Competition.
*/

#ifndef _POT_h
#define _POT_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
/*!
\class Pot
\brief  This class takes care of conversions between the IIT RMC robot arm angle and the potentiometer reading.
*/
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
	void setMaxVal();
	void setMinVal();
	void setMaxVal(int potValue);
	void setArmLength(float armLength);
	void setMinVal(int potValue);
	void setAngleOffset(float angleOffset);
	void setHeightOffset(float heightOffset);
	void setMaxAngle(float newAngle);
	void setMinAngle(float newAngle);
	void setFactor();
	float raw2Angle(int raw);
	float height2Angle(int height);
	int angle2Height(float angle);
	int height2Raw(int height);
	int raw2Height(int raw);
	float pos2Angle(int pos);
	int angle2Pos(float angle);
	int pos2Raw(int pos);
	int raw2Pos(int raw);
	int angle2Raw(float angle);
	float degree2Radian(float angle);
	float radian2Degree(float radian);
	int getHeight();
	int getPos();
	float mapfloat(float x, float in_min, float in_max, float out_min, float out_max);
	String toString();
	int potPin;    // select the input pin for the potentiometer
	int maxVal;
	int minVal;
	float maxAngle;
	float minAngle;
	float factor; // pot reading/ degree
	float heightOffset; //height of the arm pivot point WRT to the ground in cetimeters
	float armLength; //in cetimeters
	float foreArmLength = 53; //in cetimeters
	float angleOffset;
};

extern PotClass Pot;

#endif

