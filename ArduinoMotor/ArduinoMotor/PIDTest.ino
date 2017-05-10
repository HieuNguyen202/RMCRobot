#include "PID.h"
int leftTargetSpeed;
int rightTargetSpeed = 300;
int leftCurrentSpeed;
int rightCurrentSpeed;
int power;
PIDClass posPID(0.07, 2, 0.0001, 10);
TimerClass PIDTimer;
float Kp = 100;
float Kd = 200;
float Ki = 300;
int previous_error=0;
int integral=0;
int dt = 20;

void PIDTestSetup() {//fix this
	PIDTimer.reset();
}
//void PIDTestLoop() {//fix this
//	if (PIDTimer.getTime() > dt)
//	{
//		int error = rightTargetSpeed - testEncoder.v1;
//
//		integral = integral + error*dt;
//		double derivative = (error - previous_error) / (double)dt;
//		power = power + Kp*error + Ki*integral + Kd*derivative;
//		Serial.println("Erro " + String(error) + " Drev " + String(Kd*derivative));
//		previous_error = error;
//		if (power>127)
//		{
//			power = 127;
//		}
//		ST.drive(power);
//	}
//}


