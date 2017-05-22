#include "RMCArmSabertooth.h"
#include "RMCMotorSabertooth.h"
#include "Timer.h"



void setup() {
	Serial.begin(9600);
	Serial.println("Motor test begin!");
	RMCArmSabertoothTestSetup();
	//PotTestSetup();

	//RMCArmSabertoothTestSetup();
}
void loop() {
	RMCArmSabertoothTestLoop();
	//PotTestLoop();
	//delay(10);
	//RMCArmSabertoothTestLoop();
}


