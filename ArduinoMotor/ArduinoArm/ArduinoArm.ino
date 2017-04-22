/*
 Name:		ArduinoArm.ino
 Created:	4/21/2017 7:10:43 PM
 Author:	edwar
*/
int potPin = 0;    // select the input pin for the potentiometer
int val;
// the setup function runs once when you press reset or power the board
void setup() {
	Serial.begin(9600);
}

// the loop function runs over and over again until power down or reset
void loop() {
	val = analogRead(potPin);    // read the value from the sensor
	Serial.println(val);
}
