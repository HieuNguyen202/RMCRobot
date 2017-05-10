// SabertoothControllers.h

#ifndef _SABERTOOTHCONTROLLERS_h
#define _SABERTOOTHCONTROLLERS_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
	#include <Sabertooth.h> //Must be in local library
#else
	#include "WProgram.h"
#endif

class SabertoothControllersClass
{
 protected:
	 
	 

 public:
	void init();
	Sabertooth motor;
	Sabertooth arm;
	Sabertooth hand;
	SabertoothControllersClass();
	SabertoothControllersClass(int motorAddress, int armAddress, int handAddress);
	void init(int motorAddress, int armAddress, int handAddress);
	void setAddress(int motorAddress, int armAddress, int handAddress);
};

extern SabertoothControllersClass SabertoothControllers;

#endif

