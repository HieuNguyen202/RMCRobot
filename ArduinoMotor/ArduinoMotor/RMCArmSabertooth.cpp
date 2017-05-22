// 
// 
// 

#include "RMCArmSabertooth.h"

RMCArmSabertoothClass::RMCArmSabertoothClass() //never user default constructor
	:RMCSabertoothClass(128, power_mode)
{}
RMCArmSabertoothClass::RMCArmSabertoothClass(byte address, byte initialMode, int updatePeriod, PotClass leftArmPot, PotClass rightArmPot, PIDClass posPID, PIDClass syncPID)
	:RMCSabertoothClass(address, initialMode)
{
	init(updatePeriod, leftArmPot, rightArmPot, posPID, syncPID);
}
void RMCArmSabertoothClass::init(int updatePeriod, PotClass leftArmPot, PotClass rightArmPot, PIDClass posPID, PIDClass syncPID)
{
	this->leftArmPot = leftArmPot;
	this->rightArmPot = rightArmPot;
	this->posPID = posPID;
	this->syncPID = syncPID;
	int power; //arm or hand
	MAX_HEIGHT = rightArmPot.angle2Height(rightArmPot.maxAngle); //in centimeter
	MIN_HEIGHT = rightArmPot.angle2Height(rightArmPot.minAngle); //in centimeter
	MAX_ANGLE=rightArmPot.maxAngle; //in degrees
	MIN_ANGLE= rightArmPot.minAngle; //in degrees
	targetPos=rightArmPot.getPos(); //implement getPos in Pot
	targetAngle = rightArmPot.getAngle();
	targetHeight = rightArmPot.getHeight();
	power = 0;
	posPID.timer.reset();
	if (updatePeriod>0)
	{
		this->updatePeriod = updatePeriod;
	}
	else
	{
		this->updatePeriod = DEFAULT_UPDATE_PERIOD;
	}
}
/*!
Sets target position of the actuator and change mode to position mode.
\param targetPos The target position of the two actuators. Ranging from 0 to 100.
\implementation Update targetPos. Set mode to position mode.
*/
void RMCArmSabertoothClass::setPos(int targetPos)
{
	if (targetPos < 0) targetPos = 0;
	if (targetPos > 100) targetPos = 100;
	this->targetPos = targetPos;
	setMode(position_mode);
}
/*!
Sets target height of the arm and change mode to height mode.
\param targetHeight The target height of the arm. Ranging from MIN_HEIGHT to MAX_HEIGHT.
\implementation Update targetHeight. Set mode to height mode.
*/
void RMCArmSabertoothClass::setHeight(int targetHeight)
{
	if (targetHeight < MIN_HEIGHT) targetHeight = MIN_HEIGHT;
	if (targetHeight > MAX_HEIGHT) targetHeight = MAX_HEIGHT;
	this->targetHeight = targetHeight;
	setMode(height_mode);
}
/*!
Sets target angle of the arm and change mode to angle mode.
\param targetAngle The target angle of the arm. Ranging from MIN_ANGLE to MIN_ANGLE.
\implementation Update targetAngle. Set mode to angle mode.
*/
void RMCArmSabertoothClass::setAngle(float targetAngle)
{
	if (targetAngle < MIN_ANGLE) targetAngle = MIN_ANGLE;
	if (targetAngle > MAX_ANGLE) targetAngle = MAX_ANGLE;
	this->targetAngle = targetAngle;
	setMode(angle_mode);
}
/*!
Sets power of the arm’s actuators, then change mode to angle mode.
\param power The power for both arm’s actuators. Ranging from -127 to 127.
\implementation Update power. Set mode to power mode. PID to sync two actuators.
*/
void RMCArmSabertoothClass::setPower(int power)
{
	if (power < -127) power = -127;
	if (power > 127) power = 127;
	this->power = power;
	setMode(power_mode);
}
/*!
Sets power of the arm’s actuators, then change mode to raw mode.
\param raw The raw value of the arm. Pos pot.
\implementation Update power. Set mode to raw mode. PID to sync two actuators.
*/
void RMCArmSabertoothClass::setRaw(int targetRaw)
{
	if (targetRaw >= 0 && targetRaw <= 1023)
	{
		this->targetRaw = targetRaw;
		setMode(raw_mode);
	}
}
/*!
Sets left and right actuator power to achieve either power, position, height and angle targets.
\implementation Switch on mode. Need to sync the motor.
Case power: check timer, drive with lPower and rPower
Case position: check timer, PID to get the needed power to achieve the target position.
Case height: check timer, PID to get the needed power to achieve the target height.
Case angle: check timer, PID to get the needed power to achieve the target height.
Default: Stop to actuators.
*/
void RMCArmSabertoothClass::Update()
{
	switch (mode)
	{
	case power_mode:
		sabertooth->motor(1, power);
		sabertooth->motor(2, power);//adjusted power
		break;
	default:
		if (posPID.timer.getTime() > updatePeriod)
		{
			int targetPotVal;
			switch (mode)
			{
			case angle_mode:
				targetPotVal = rightArmPot.angle2Raw(targetAngle);
				break;
			case height_mode:
				targetPotVal = rightArmPot.height2Raw(targetHeight);
				break;
			case position_mode:
				targetPotVal = rightArmPot.pos2Raw(targetPos);
				break;
			case raw_mode:
				targetPotVal = targetRaw;
				break;
			}
			int tempPower = posPID.getPower(rightArmPot.getValue(), targetPotVal);
			Serial.println("Power: "+String(tempPower)+" Currebt Raw: " + String(rightArmPot.getValue()) + " target Raw: " + String(targetPotVal));
			//sabertooth->motor(1, tempPower);
			sabertooth->motor(2, tempPower);//adjusted power
		}
		break;
	}
}
String RMCArmSabertoothClass::toString()
{
	return "power:[" + String(power) + "] targetPos:[" + String(targetPos)
		+ "] targetAngle:[" + String(targetAngle) + "] targetHeight:[" + String(targetHeight) + "]"
		+ "] updatePeriod:[" + String(updatePeriod) + "] MAX_HEIGHT:[" + String(MAX_HEIGHT)
		+ "] MIN_HEIGHT:[" + String(MIN_HEIGHT) + "]" + "] MAX_ANGLE:[" + String(MAX_ANGLE)
		+ "] MIN_ANGLE:[" + String(MIN_ANGLE);
}
RMCArmSabertoothClass RMCArmSabertooth;

