// Author: Hieu Nguyen
// Email: hnguye19@hawk.iit.edu
// Notes: Pin numbers must be hard coded in order for DigialReadFast and DigitalWriteFast work, use #define
#include "SpeedEncoder.h"
#include <digitalWriteFast.h>

#define _gPin1 2 //Green wire of encoder 1
#define _wPin1 10 //White wire of encoder 1
#define _gPin2 3 //Green wire of encoder 2
#define _wPin2 13 //White wire of encoder 2
SpeedEncoderClass::SpeedEncoderClass()
{
	pinMode(_gPin1, INPUT_PULLUP);
	pinMode(_wPin1, INPUT_PULLUP);
	pinMode(_gPin2, INPUT_PULLUP);
	pinMode(_wPin2, INPUT_PULLUP);
	pinModeFast(_gPin1, INPUT_PULLUP);
	pinModeFast(_wPin1, INPUT_PULLUP);
	pinModeFast(_gPin2, INPUT_PULLUP);
	pinModeFast(_wPin2, INPUT_PULLUP);
	count1 = 0;
	count2 = 0;
	v1 = 0;
	v2 = 0;
	interval = 10;
}
void SpeedEncoderClass::attach(voidFuncPtr interuptFunction1, voidFuncPtr interuptFunction2)
{
	attachInterrupt(digitalPinToInterrupt(_gPin1), interuptFunction1, RISING);
	attachInterrupt(digitalPinToInterrupt(_gPin2), interuptFunction2, RISING);
}
void SpeedEncoderClass::rise1()
{
	count1 += digitalReadFast(_wPin1) ? 1 : -1;
}
void SpeedEncoderClass::rise2()
{
	count2 += digitalReadFast(_wPin2) ? 1 : -1;
}
void SpeedEncoderClass::updateSpeed()//not tested
{
	if (timer.getTime() >= interval)
	{
		v1 = count1 - lastCount1;
		lastCount1 = count1;
		v2 = count2 - lastCount2;
		lastCount2 = count2;
		timer.reset();
	}
}
SpeedEncoderClass SpeedEncoder;

