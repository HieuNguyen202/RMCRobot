#include "PID.h"
/*!
Constructor. Initilizes a PID object with given constants and period.
\param Kp PID propotional constant.
\param Kd PID derivative constant.
\param Ki PID integral constant.
\param dt update period.
*/
PIDClass::PIDClass()
{
	init(0.07, 2, 0.0001, 10);
}
/*!
Constructor. Initilizes a PID object with given constants and period.
\param Kp PID propotional constant.
\param Kd PID derivative constant.
\param Ki PID integral constant.
\param dt update period.
*/
PIDClass::PIDClass(float Kp, float Kd, float Ki, int dt)
{
	init(Kp, Kd, Ki, dt);
}
void PIDClass::init(float Kp, float Kd, float Ki, int dt)
{
	previous_error = 0;
	integral = 0;
	power = 0;
	accPower = 0;
	if (dt > 0) this->dt = dt;
	if (Kp > 0) this->Kp = Kp;
	if (Kd > 0) this->Kd = Kd;
	if (Ki > 0) this->Ki = Ki;
}
/*!
Gets the Sabertooth's power needed to maintain a target speed.
\param current the current speed of a motor.
\param target the target speed of a motor.
\return Sabertooth's motor power from -127 to 127
*/
int PIDClass::getAccPower(int current, int target) //Accumulative power for speed control
{
	if (timer.getTime() > dt)
	{
		accPower = accPower + getPower(current, target);
	}
	return accPower;
}
/*!
Gets the Sabertooth's power needed to get to a target position.
\param current the current posision of a linear actuator.
\param target the target posision of a linear actuator.
\return Sabertooth's motor power from -127 to 127
*/
int PIDClass::getPower(int current, int target)
{
	if (timer.getTime() > dt)
	{
		int error = target - current;
		integral = integral + error*dt;
		double derivative = (error - previous_error) / (double)dt;
		power = Kp*error + Ki*integral + Kd*derivative;
		previous_error = error;
		timer.reset();		
	}
	return power;
} //for position control
/*!
\return PID constants: Kp, Kd, Ki and update period dt in miliseconds.
*/
String PIDClass::toString()
{
	return "Kp:[" + String(Kp) + "] Kd:[" + String(Kd) + "] Ki:[" + String(Ki) + "] dt:[" + String(dt) + "]";
}
PIDClass PID;
