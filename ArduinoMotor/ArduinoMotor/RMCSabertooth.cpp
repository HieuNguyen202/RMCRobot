// 
// 
// 
#include "RMCSabertooth.h"
RMCSabertoothClass::RMCSabertoothClass()
{
	init(128,0);
}
RMCSabertoothClass::RMCSabertoothClass(byte address, byte initalMode)
{
	init(address, initalMode);
}
void RMCSabertoothClass::init(byte address, byte initalMode)
{
	setAddress(address);
	setMode(initalMode);
}
/*!
Sets a new Sabertooth address that this object to controlling.
\param address The new address. Ranging from 128 to 135. Default is 128.
*/
void RMCSabertoothClass::setAddress(byte address)
{
	if (address!=this->address && address>=128 &&address<=135)
	{
		sabertooth = new Sabertooth(address);
		
	}
	else
	{
		sabertooth = new Sabertooth(128);
	}
	this->address = address;
}
/*!
Sets driving mode to either power, speed, position, angle, or height.
\param mode The mode the robot will run on in next update period. 0: power, 1: speed, 2: position, 3 angle, 4: height.
\implementation Make sure mode is either 0, 1, 2, or 4. Assign new mode to mode. Default is power mode (0).
*/
void RMCSabertoothClass::setMode(byte mode) {
	if (mode>=0 && mode <=4)
	{
		this->mode = mode;
	}
	else
	{
		this->mode = 0;
	}
}
RMCSabertoothClass RMCSabertooth;

