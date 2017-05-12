#include "Pot.h"
PotClass rightArmPot(0);
void PotTestSetup() {
	rightArmPot.setMaxVal(347);
	rightArmPot.setMinVal(77);
	rightArmPot.setMaxAngle(55);
	rightArmPot.setMinAngle(-15);
	rightArmPot.setArmLength(85.943);
	rightArmPot.setAngleOffset(-20);
	rightArmPot.setHeightOffset(50);


}
void PotTestLoop() {
	Serial.println(rightArmPot.toString());
}


