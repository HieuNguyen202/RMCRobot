//!  PID Class. 
/*!
This is class is written for the IIT's mining robot who competes in NASA Robotic Mining Competition.
*/

#ifndef _PID_h
#define _PID_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
	
#else
	#include "WProgram.h"
#endif
#include "Timer.h"
/*!
\class PID
\brief  A implimentation of the PID control system. PID is a close loop control system
		that allows the robot to adjust itself to achieve a set goal.
*/
class PIDClass
{
 protected:

 public:
	int previous_error;
	int integral;
	int dt;
	float Kp;
	float Kd;
	float Ki;
	PIDClass();
	PIDClass(float Kp, float Kd, float Ki, int dt);
	void init(float Kp, float Kd, float Ki, int dt);
	int getAccPower(int current, int target);
	int getPower(int current, int target);
	String toString();
	int power;
	int accPower;
	TimerClass timer;
};
extern PIDClass PID;

#endif

