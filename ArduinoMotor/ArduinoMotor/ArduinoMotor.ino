#include "Pot.h"
#include "PID.h"
#include "I2C.h"
#include "Timer.h"
#include "SpeedEncoder.h"
#include <Wire.h>
#include "digitalWriteFast.h"
#include "Sabertooth.h"
#include "Timer.h"

int leftTargetSpeed;
int rightTargetSpeed = 300;
int leftCurrentSpeed;
int rightCurrentSpeed;
int power;

TimerClass timer;
TimerClass timer2;
SpeedEncoderClass encoder12;
I2CClass i2c12(7);
Sabertooth ST(130);
PIDClass posPID(0.07, 2, 0.0001, 10);
PotClass armPot();

//PID
int previous_error = 0;
int integral = 0;
int dt = 20;
double Kp = 0.07;
double Kd = 2;
double Ki = 0.0001;

void setup() {
	Serial.begin(9600);           // set up serial library at 9600 bps
	Serial.println("Motor test begin!");
	//Encoder setup
	encoder12.attach(rise1, rise2); //attachInterupt for pin 2 and 3
									//i2c setup
	i2c12.attach(receiveData, sendData);

	//Sabertooth
	//SabertoothTXPinSerial.begin(9600);
	//ST.drive(0);
	//ST.turn(0);
	ST.drive(50);
	ST.turn(50);
	timer.reset();
	timer2.reset();
	pinMode(0, OUTPUT);  // declare the ledPin as an OUTPUT
	pinMode(1, OUTPUT);  // declare the ledPin as an OUTPUT

}
void loop() {
	encoder12.updateSpeed();
	//Motor
	//drive(-75, -75);
	//Encoder
	if (timer.getTime()>100)
	{
		//Serial.println("hieu"+String(Kd*derivative));
		int pot0 = analogRead(0);
		int pot1 = analogRead(1);
		//Ki = pot0/7500.;
		//Kd = pot1;
	}
	//ST.drive(127);
	//i2c
	//Serial.println("leftTargetSpeed: " + String(i2c12.leftTargetSpeed) + " rightTargetSpeed: " + String(i2c12.rightTargetSpeed) );

	//Sabertooth

	//// Don't turn. Ramp from going backwards to going forwards, waiting 20 ms (1/50th of a second) per value.



	//if (timer.getTime() > 1)
	//{
	//	long currentSpeed = encoder12.v1;
	//	if (currentSpeed<rightTargetSpeed-50)
	//	{
	//		power++;
	//	}
	//	else if (currentSpeed>rightTargetSpeed+50)
	//	{
	//		power--;
	//	}
	//	else
	//	{
	//	}
	//	if (power>127)
	//	{
	//		power = 127;
	//	}
	//	else if (power<-127)
	//	{
	//		power = -127;
	//	}
	//	ST.drive(power);
	//	timer.reset();
	//}
}
//Encoder
void rise1() {
	encoder12.rise1();
}
void rise2() {
	encoder12.rise2();
}

//i2c
void receiveData(int byteCount) {
	i2c12.receiveData(byteCount);
}
void sendData() {//fix this
	i2c12.sendData();
}

//PID
void PIDTest() {//fix this
	if (timer.getTime() > dt)
	{
		int error = rightTargetSpeed - encoder12.v1;

		integral = integral + error*dt;
		double derivative = (error - previous_error) / (double)dt;
		power = power + Kp*error + Ki*integral + Kd*derivative;
		//Serial.println("Erro " + String(error) + " Drev " + String(Kd*derivative));
		previous_error = error;
		if (power>127)
		{
			power = 127;
		}
		ST.drive(power);
	}
}
//motor