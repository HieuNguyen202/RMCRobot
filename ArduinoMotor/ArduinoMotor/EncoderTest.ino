#include "SpeedEncoder.h"
SpeedEncoderClass testEncoder;
TimerClass encoderTimer;
void EncoderTestSetup()
{
	encoderTimer.reset();
	testEncoder.attach(rise1, rise2); //attachInterupt for pin 2 and 3
}
void EncoderTestLoop()
{
	testEncoder.updateSpeed();
}
void rise1() {
	testEncoder.rise1();
}
void rise2() {
	testEncoder.rise2();
}

