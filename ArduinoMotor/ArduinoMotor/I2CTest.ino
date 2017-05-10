//This is the official code. Don't delete.
#include <Wire.h>
/*
RPI               Arduino Uno		Arduino Mega
--------------------------------------------
GPIO 2 (SDA) <--> Pin A4 (SDA)		Pin 20 (SDA)	Green
GPIO 3 (SCL) <--> Pin A5 (SCL)		Pin 21 (SCL)	Yellow
Ground       <--> Ground			Ground			Black
*/

#define I2CAddress 7

#define is_connected 0
#define set_arm_address 1
#define set_hand_address 2
#define set_arm_height 3
#define set_arm_height_offset 4
#define set_arm_angle 5
#define set_arm_angle_offset 6
#define set_motor_speed 7
#define set_motor_power 8
#define set_arm_power 9
#define set_hand_power 10
#define set_hand_angle 11
#define set_hand_angle_offset 12
#define set_hand_height 13
#define set_hand_height_offset 14
#define set_motor_address 15
#define stop_motor 16
#define stop_arm 17
#define stop_hand 18
void I2CTestSetup()
{
	Wire.begin(I2CAddress);
	Wire.onReceive(onI2CReceive);
	Wire.onRequest(onI2CRequest);
}
void I2CTestLoop() {
}
void onI2CReceive(int byteCount) {
	int message[8];
	int i = 0;
	while (Wire.available()) {
		message[i] = Wire.read();
		i++;
	}
	run(message);
}
void onI2CRequest() {//fix this
	Wire.write(0);
}
void run(int message[]) {//Execute message sent via I2C protocol
	int command = message[0];
	switch (command)
	{
	case  is_connected:
		Serial.println(is_connected); break;
	case  set_arm_address:
		Serial.println(set_arm_address); break;
	case  set_hand_address:
		Serial.println(set_hand_address); break;
	case  set_arm_height:
		Serial.println(set_arm_height); break;
	case  set_arm_height_offset:
		Serial.println(set_arm_height_offset); break;
	case  set_arm_angle:
		Serial.println(set_arm_angle); break;
	case  set_arm_angle_offset:
		Serial.println(set_arm_angle_offset); break;
	case  set_motor_speed:
		Serial.println(set_motor_speed); break;
	case  set_motor_power:
		Serial.println(set_motor_power); break;
	case  set_arm_power:
		Serial.println(set_arm_power); break;
	case  set_hand_power:
		Serial.println(set_hand_power); break;
	case  set_hand_angle:
		Serial.println(set_hand_angle); break;
	case  set_hand_angle_offset:
		Serial.println(set_hand_angle_offset); break;
	case  set_hand_height:
		Serial.println(set_hand_height); break;
	case  set_hand_height_offset:
		Serial.println(set_hand_height_offset); break;
	case  set_motor_address:
		Serial.println(set_motor_address); break;
	case  stop_motor:
		Serial.println(stop_motor); break;
	case  stop_arm:
		Serial.println(stop_arm); break;
	case  stop_hand:
		Serial.println(stop_hand); break;
	default:
		break;
	}
}

