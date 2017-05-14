#include "Pot.h"
PotClass rightArmPot(0);
PotClass leftArmPot(1);
void PotTestSetup() {
	//rightArmPot.setMaxVal(350);
	//rightArmPot.setMinVal(77);
	//rightArmPot.setMaxAngle(56);
	//rightArmPot.setMinAngle(-15.4);
	rightArmPot.setZeroVal(136);
	rightArmPot.setArmLength(86.5);
	//rightArmPot.setAngleOffset(-20);

}
void PotTestLoop() {
	Serial.println(rightArmPot.toStringLite());
}


