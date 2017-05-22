// RMCArmSabertooth.h

#ifndef _RMCARMSABERTOOTH_h
#define _RMCARMSABERTOOTH_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
#include "RMCSabertooth.h"
#include "Timer.h"
#include "Pot.h"
#include "PID.h"

class RMCArmSabertoothClass :public RMCSabertoothClass
{
 protected:

 public:
	PIDClass posPID;
	PIDClass syncPID;
	PotClass leftArmPot;
	PotClass rightArmPot;
	int power; //arm or hand
	int targetPos;  //arm or hand
	float targetAngle; //arm and hand
	int targetHeight; //arm and hand
	int updatePeriod;
	int targetRaw;
	int DEFAULT_UPDATE_PERIOD = 20;
	int MAX_HEIGHT; //in centimeter
	int MIN_HEIGHT; //in centimeter
	float MAX_ANGLE; //in degrees
	float MIN_ANGLE; //in degrees

	RMCArmSabertoothClass();
	RMCArmSabertoothClass(byte address, byte initialMode, int updatePeriod, PotClass leftArmPot, PotClass rightArmPot, PIDClass posPID, PIDClass syncPID);
	void init(int updatePeriod, PotClass leftArmPot, PotClass rightArmPot, PIDClass posPID, PIDClass syncPID);

	void setPos(int targetPos);
	void setHeight(int targetHeight);
	void setAngle(float targetAngle);
	void setPower(int targetPower);
	void setRaw(int raw);
	String toString();
	void Update();


};

extern RMCArmSabertoothClass RMCArmSabertooth;

#endif

