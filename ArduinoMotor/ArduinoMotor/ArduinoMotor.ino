#include "RMCArmSabertooth.h"
#include "RMCMotorSabertooth.h"
#include "Timer.h"



void setup() {
	Serial.begin(9600);
	Serial.println("Motor test begin!");
	PotTestSetup();

	//RMCArmSabertoothTestSetup();
}
void loop() {
	PotTestLoop();
	delay(10);
	//RMCArmSabertoothTestLoop();
}


