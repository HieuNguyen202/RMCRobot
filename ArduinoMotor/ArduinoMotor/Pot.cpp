// 
// 
// 

#include "Pot.h"
PotClass::PotClass(int potPin)
{
	init(potPin);
}
PotClass::PotClass()
{
	init(0);
}
void PotClass::init(int potPin)
{
	if (potPin>=0)
	{
		this->potPin = potPin;
	}
}
int PotClass::getRawValue() {
	return analogRead(potPin);    // read the value from the sensor
}
int PotClass::getValue() {
	return getRawValue();    //handle error when the pot is unpluged.
}
float PotClass::getAngle() {
	return raw2Angle(getRawValue());    //handle error when the pot is unpluged.
}
void PotClass::setMax() {
	max= getRawValue();    // read the value from the sensor
}
void PotClass::setMin() {
	min = getRawValue();    // read the value from the sensor
}
void PotClass::setMaxAngle(float newAngle) {
	if (newAngle>=-180&&newAngle<=180)
	{
		maxAngle = newAngle;    // read the value from the sensor
	}
}
void PotClass::setMinAngle(float newAngle) {
	if (newAngle >= -180 && newAngle <= 180)
	{
		minAngle = newAngle;    // read the value from the sensor
	}
}
void PotClass::setFactor() {
	factor = (max - min) / (maxAngle - minAngle);
}
float PotClass::raw2Angle(int raw) {
	return mapfloat(raw, min, max, minAngle, maxAngle);
}
int PotClass::angle2Raw(float angle) {
	return (int)mapfloat(angle, minAngle, maxAngle, min, max);
}
float PotClass::mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
String PotClass::toString()
{
	return "raw:[" + String(getRawValue()) + "] Angle:[" + String(getAngle()) + "] Min:[" + String(min) + "] Max:[" + String(max) + "]" + "] MinAngle:[" + String(minAngle) + "] MaxAngle:[" + String(maxAngle) + "]";
}
PotClass Pot;