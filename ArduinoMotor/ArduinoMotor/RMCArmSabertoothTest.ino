#include "RMCArmSabertooth.h"
PotClass myRightArmPot(0);
PotClass myLeftArmPot(1);
PIDClass myPosPID(5.3f, 150.0f, 0.005f, 20);
PIDClass mySyncPID(1.1f, 0.1f, 0.1f, 20);
RMCArmSabertoothClass arm((byte)131, 0, 20, myLeftArmPot, myRightArmPot, myPosPID, mySyncPID);

void RMCArmSabertoothTestSetup()
{
	arm.setRaw(100);
}
void RMCArmSabertoothTestLoop()
{
	arm.Update();
}