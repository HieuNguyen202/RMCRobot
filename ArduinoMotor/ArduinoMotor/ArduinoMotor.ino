//#include "SabertoothControllers.h"
//#include "Pot.h"
//#include "PID.h"
//#include "I2C.h"
//#include "Timer.h"
#include "RMCSabertooth.h"
#include <Wire.h> //built-in library
///#include <Sabertooth.h> //Must be in local library
//#include "Timer.h"

int leftTargetSpeed;
int rightTargetSpeed = 300;
int leftCurrentSpeed;
int rightCurrentSpeed;
int power;






//TimerClass timer2;


//PIDClass posPID(0.07, 2, 0.0001, 10);
//PotClass armPot();



void setup() {
	Serial.begin(9600);
	Serial.println("Motor test begin!");

	//Sabertooth

	//ST.drive(0);
	//ST.turn(0);
	//ST.drive(50);
	//ST.turn(50);
	
	//timer2.reset();
	//pinMode(0, OUTPUT);  // declare the ledPin as an OUTPUT
	//pinMode(1, OUTPUT);  // declare the ledPin as an OUTPUT

}
void loop() {

	//Motor
	//drive(-75, -75);

	//i2c
	//Serial.println("leftTargetSpeed: " + String(i2c12.leftTargetSpeed) + " rightTargetSpeed: " + String(i2c12.rightTargetSpeed) );

	//Sabertooth

	//// Don't turn. Ramp from going backwards to going forwards, waiting 20 ms (1/50th of a second) per value.


}


//PID
//void PIDTest() {//fix this
//	if (timer.getTime() > dt)
//	{
//		int error = rightTargetSpeed - encoder12.v1;
//
//		integral = integral + error*dt;
//		double derivative = (error - previous_error) / (double)dt;
//		power = power + Kp*error + Ki*integral + Kd*derivative;
//		//Serial.println("Erro " + String(error) + " Drev " + String(Kd*derivative));
//		previous_error = error;
//		if (power>127)
//		{
//			power = 127;
//		}
//		ST.drive(power);
//	}
//}
//motor