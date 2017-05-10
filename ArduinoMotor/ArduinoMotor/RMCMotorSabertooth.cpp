// 
// 
// 

#include "RMCMotorSabertooth.h"
RMCMotorSabertoothClass::RMCMotorSabertoothClass() {}
RMCMotorSabertoothClass::RMCMotorSabertoothClass(byte address, byte initialMode, int speedUpdatePeriod) 
	:RMCSabertoothClass(address, initialMode)
{
	init(speedUpdatePeriod);
}
void RMCMotorSabertoothClass::init(int speedUpdatePeriod)
{
	leftTargetSpeed = 0;
	rightTargetSpeed=0;
	lPower=0;
	rPower=0;
	speedTimer.reset();
	if (speedUpdatePeriod>0)
	{
		this->speedUpdatePeriod = speedUpdatePeriod;
	}
	else
	{
		this->speedUpdatePeriod = DEFAULT_UPDATE_PERIOD;
	}
}
/*!
Sets left and right motor power to the given power levels.
\param lPower The power for left motor. Possible values: from -127 to 127.
\param rPower The power for right motor. Possible values: from -127 to 127.
\implementation Update lPower and rPower. Set mode to power mode.
*/
void RMCMotorSabertoothClass::setMotorPower(int lPower, int rPower)
{
	if (lPower < -127) lPower = -127;
	if (lPower > 127) lPower = 127;
	if (rPower < -127) rPower = -127;
	if (rPower > 127) rPower = 127;
	this->lPower = lPower;
	this->rPower = rPower;
	setMode(power_mode);
}
/*!
Sets left and right motor power to the given power levels.
\param lSpeed The speed for left motor. Possible values: from -max to max.
\param rSpeed The speed for right motor. Possible values: from -max to max.
\implementation Update lSpeed and rSpeed. Set mode to speed mode.
*/
void RMCMotorSabertoothClass::setMotorSpeed(int leftTargetSpeed, int rightTargetSpeed)
{
	this->leftTargetSpeed = leftTargetSpeed;
	this->rightTargetSpeed = rightTargetSpeed;
	setMode(speed_mode);
}
/*!
Sets left and right motor power to achieve either speed targets or power targets.
\implementation Switch on mode.
Case power: check timer, drive with lPower and rPower
Case speed: check timer, PID to get the needed power to achieve the target speeds.
Default: Stop to motors.
*/
void RMCMotorSabertoothClass::Update()
{
	switch (mode)
	{
	case power_mode:
		sabertooth->motor(1, lPower);
		sabertooth->motor(2, rPower);
	case speed_mode:
		if (speedTimer.getTime()>speedUpdatePeriod)
		{
			//add more codes here
			speedTimer.reset();
		}
		//
	default:
		break;
	}

}

RMCMotorSabertoothClass RMCMotorSabertooth;

