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
	maxVal= getRawValue();    // read the value from the sensor
}
/*!
Sets the potentiometer's value that is associated with the robot arm's lowest angle.
The current potentiometer's raw value will be used automatically.
*/
void PotClass::setMinVal() {
	minVal = getRawValue();    // read the value from the sensor
}
/*!
Sets the potentiometer's value that is associated with the robot arm's highest angle.
\param potValue the potentiometer's raw value that is determined to be the max.
*/
void PotClass::setMaxVal(int potValue) {
	if (potValue>=0)
	{
		maxVal = potValue;    // read the value from the sensor
	}
}
/*!
Sets the potentiometer's value that is associated with the robot arm's lowest angle.
\param potValue the potentiometer's raw value that is determined to be the min.
*/
void PotClass::setMinVal(int potValue) {
	if (potValue >= 0)
	{
		minVal = potValue;    // read the value from the sensor
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
	factor = (maxVal - minVal) / (maxAngle - minAngle);
}
/*!
Converts shovel's height to a robot arm's angle.
\param height the shovel's height
\return the equivalent robot arm's angle
*/
float PotClass::height2Angle(int height) {
	return height*0.1;//find formula for this
}
/*!
Converts the robot arm's angle to shovel's height.
\param angle robot arm's angle
\return the shovel's height
*/
int PotClass::angle2Height(float angle) {
	//float heightFromParallel = (armLength*sin(degree2Radian(getAngle())));
	//return (shoulderHeight + heightFromParallel);
	return angle*0.1;//find formula for this
}
/*!
Converts shovel's height to a robot arm's angle.
\param height the shovel's height
\return the equivalent potentiometer value.
*/
int PotClass::height2Raw(int height) {
	return angle2Raw(height2Angle(height));
}
/*!
Converts shovel's height to a robot arm's angle.
\param height the shovel's height
\return the equivalent potentiometer value.
*/
int PotClass::raw2Height(int raw) {
	return angle2Height(raw2Angle(raw));
}
/*!
Converts actuator's position to a robot arm's angle.
\param pos actuator's position
\return the equivalent robot arm's angle
*/
float PotClass::pos2Angle(int pos) {
	return pos*0.1;//find formula for this
}
int PotClass::angle2Pos(float angle) {
	return angle*0.1;//find formula for this
}
/*!
Converts actuator's position to an equivelant potentiometer value.
\param pos actuator's position
\return the equivalent potentiometer value.
*/
int PotClass::pos2Raw(int pos) {
	return angle2Raw(pos2Angle(pos));
}
/*!
Converts actuator's position to an equivelant potentiometer value.
\param pos actuator's position
\return the equivalent potentiometer value.
*/
int PotClass::raw2Pos(int raw) {
	return angle2Pos(raw2Angle(raw));
}
/*!
Converts a desired robot's arm angle to an equivelant potentiometer value.
\param angle the desired robot's arm angle.
\return the equivalent potentiometer value.
*/
int PotClass::angle2Raw(float angle) {
	return (int)mapfloat(angle, minAngle, maxAngle, minVal, maxVal);
}
/*!
Converts a potentiometer's raw value to a robot arm's angle.
\param angle the potentiometer's raw value
\return the equivalent robot arm's angle
*/
float PotClass::raw2Angle(int raw) {
	return mapfloat(raw, minVal, maxVal, minAngle, maxAngle);
}
float PotClass::degree2Radian(float angle) {
	return (angle*(PI / 180));
}
float PotClass::radian2Degree(float radian) {
	return (radian*(180 / PI));
}
int PotClass::getHeight() {
	return raw2Height(getValue());
}
int PotClass::getPos() {
	return raw2Pos(getValue());
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
	return "raw:[" + String(getRawValue()) + "] Angle:[" + String(getAngle())
		+ "] Height:[" + String(getHeight()) + "] Pos:[" + String(getPos()) + "] MinVal:["
		+ String(minVal) + "] MaxVal:[" + String(maxVal) + "]" + "] MinAngle:[" + String(minAngle)
		+ "] MaxAngle:[" + String(maxAngle) + "] MaxHeight:[" + String(raw2Height(maxVal))
		+ "] MinHeight:[" + String(raw2Height(minVal)) + "] MaxHeight:[" + String(raw2Height(maxVal))
		+ "] MaxPos:[" + String(raw2Pos(maxVal)) + "] MinPos:[" + String(raw2Pos(minVal));
}
PotClass Pot;