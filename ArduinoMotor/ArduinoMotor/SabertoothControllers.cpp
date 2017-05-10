// 
// 
// 

#include "SabertoothControllers.h"
SabertoothControllersClass::SabertoothControllersClass()
{
	Sabertooth motor(130);
	Sabertooth arm(131);
	Sabertooth hand(132);
}
SabertoothControllersClass::SabertoothControllersClass(int motorAddress, int armAddress, int handAddress)
{
	init(motorAddress, armAddress, handAddress);
}
void SabertoothControllersClass::init(int motorAddress, int armAddress, int handAddress)
{
	Sabertooth motor(motorAddress);
	Sabertooth arm(armAddress);
	Sabertooth hand(handAddress);
}
void SabertoothControllersClass::setAddress(int motorAddress, int armAddress, int handAddress)
{
	Sabertooth motor(motorAddress);
	Sabertooth arm(armAddress);
	Sabertooth hand(handAddress);
}


SabertoothControllersClass SabertoothControllers;

