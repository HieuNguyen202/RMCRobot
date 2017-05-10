Sabertooth ST(130);
TimerClass 
void SabertoothTestSetup()
{
	SabertoothTXPinSerial.begin(9600);
}
void SabertoothTestLoop()
{

}
void driveTest()
{
	if (timer.getTime() > 1)
	{
		long currentSpeed = encoder12.v1;
		if (currentSpeed<rightTargetSpeed-50)
		{
			power++;
		}
		else if (currentSpeed>rightTargetSpeed+50)
		{
			power--;
		}
		else
		{
		}
		if (power>127)
		{
			power = 127;
		}
		else if (power<-127)
		{
			power = -127;
		}
		ST.drive(power);
		timer.reset();
	}
}