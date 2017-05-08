// 
// 
// 

#include "I2C.h"
I2CClass::I2CClass(int address)
{
	_address = address;
	init();
}
I2CClass::I2CClass()//fix this
{
}
void I2CClass::init()
{
	Wire.begin(_address);
}
void I2CClass::attach(voidFuncPtrInt receiveDataFunction, voidFuncPtr sendDataFunction)
{
	Wire.onReceive(receiveDataFunction);
	Wire.onRequest(sendDataFunction);
}
void I2CClass::receiveData(int byteCount) {
	int data[8];
	int i = 0;
	while (Wire.available()) {
		data[i] = Wire.read();
		i++;
	}
	if (data[0] == 1) //update left and right speed
	{
		leftTargetSpeed = data[1];
		rightTargetSpeed = data[2];
	}
}
void I2CClass::sendData() {//fix this
	Wire.write(leftTargetSpeed);
}
I2CClass I2C;