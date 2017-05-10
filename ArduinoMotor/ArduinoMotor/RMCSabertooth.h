// RMCSabertooth.h

#ifndef _RMCSABERTOOTH_h
#define _RMCSABERTOOTH_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
#include <Sabertooth.h>
#define power_mode 0
#define speed_mode 1
#define position_mode 2
#define angle_mode 3
#define height_mode 4

class RMCSabertoothClass
{
 protected:


 public:
	 RMCSabertoothClass();
	 RMCSabertoothClass(byte address, byte initalMode);

	 void init(byte address, byte initalMode);
	 void setAddress(byte address);
	 void setMode(byte mode);
	 Sabertooth *sabertooth;
	 byte address;
	 byte mode;

};

extern RMCSabertoothClass RMCSabertooth;

#endif

