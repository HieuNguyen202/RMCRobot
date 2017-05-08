// 
// 
// 

#include "Pot.h"
/*!
Constructor. Initilizes pot pin number.
\param potPin the Arduino analog pin number. Default is 0.
*/
PotClass::PotClass(int potPin)
{
	init(potPin);
}
/*!
Constructor. Initilizes pot pin number.
\param potPin the Arduino analog pin number. Default is 0.
*/
PotClass::PotClass()
{
	init(0);
}
/*!
Initilizes pot pin number.
\param potPin the Arduino analog pin number. Default is 0.
*/
void PotClass::init(int potPin)
{
	if (potPin>=0)
	{
		this->potPin = potPin;
	}
}
/*!
Gets the pot's raw value.
\return the pot's raw value.
*/int PotClass::getRawValue() {
	return analogRead(potPin);    // read the value from the sensor
}
/*!
Gets the current pot value.
\return the current pot value.
*/
int PotClass::getValue() {
	return getRawValue();    //handle error when the pot is unpluged.
}
/*!
Gets the robot arm's angle that is equivalent to the current pot value.
\return the current robot arm's angle.
*/
float PotClass::getAngle() {
	return raw2Angle(getRawValue());    //handle error when the pot is unpluged.
}
/*!
Sets the potentiometer's value that is associated with the robot arm's highest angle.
The current potentiometer's raw value will be used automatically.
*/
void PotClass::setMax() {
	max= getRawValue();    // read the value from the sensor
}
/*!
Sets the potentiometer's value that is associated with the robot arm's lowest angle.
The current potentiometer's raw value will be used automatically.
*/
void PotClass::setMin() {
	min = getRawValue();    // read the value from the sensor
}
/*!
Sets the potentiometer's value that is associated with the robot arm's highest angle.
\param potValue the potentiometer's raw value that is determined to be the max.
*/
void PotClass::setMax(int potValue) {
	if (potValue>=0)
	{
		max = potValue;    // read the value from the sensor
	}
}
/*!
Sets the potentiometer's value that is associated with the robot arm's lowest angle.
\param potValue the potentiometer's raw value that is determined to be the min.
*/
void PotClass::setMin(int potValue) {
	if (potValue >= 0)
	{
		min = potValue;    // read the value from the sensor
	}
}
/*!
Sets the robot arm's highest angle.
\param newAngle the highest angle the robot arm can reach.
*/
void PotClass::setMaxAngle(float newAngle) {
	if (newAngle>=-180&&newAngle<=180)
	{
		maxAngle = newAngle;    // read the value from the sensor
	}
}
/*!
Sets the robot arm's lowest angle.
\param newAngle the lowest angle the robot arm can reach.
*/
void PotClass::setMinAngle(float newAngle) {
	if (newAngle >= -180 && newAngle <= 180)
	{
		minAngle = newAngle;    // read the value from the sensor
	}
}
/*!
Calculates and sets the [pot value/angle] convertion factor based on the pot's extrema.
*/
void PotClass::setFactor() {
	factor = (max - min) / (maxAngle - minAngle);
}
/*!
Converts a potentiometer's raw value to a robot arm's angle.
\param angle the potentiometer's raw value
\return the equivalent robot arm's angle
*/
float PotClass::raw2Angle(int raw) {
	return mapfloat(raw, min, max, minAngle, maxAngle);
}
/*!
Converts a desired robot's arm angle to an equivelant potentiometer value.
\param angle the desired robot's arm angle.
\return the equivalent potentiometer value.
*/
int PotClass::angle2Raw(float angle) {
	return (int)mapfloat(angle, minAngle, maxAngle, min, max);
}
float PotClass::mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
/*!
\return the current pot's raw value and its equivalant angle, pot's min and max values, and the arm's min and max angles.
*/
String PotClass::toString()
{
	return "raw:[" + String(getRawValue()) + "] Angle:[" + String(getAngle()) + "] Min:[" + String(min) + "] Max:[" + String(max) + "]" + "] MinAngle:[" + String(minAngle) + "] MaxAngle:[" + String(maxAngle) + "]";
}
PotClass Pot;