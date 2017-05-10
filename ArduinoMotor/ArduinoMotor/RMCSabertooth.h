// RMCSabertooth.h

#ifndef _RMCSABERTOOTH_h
#define _RMCSABERTOOTH_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
#include <Sabertooth.h>

class RMCSabertoothClass
{
 protected:


 public:
	void init();
	
};

extern RMCSabertoothClass RMCSabertooth;

#endif

