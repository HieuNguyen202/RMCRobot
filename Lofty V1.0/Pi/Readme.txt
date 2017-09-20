Put this in the robot computer (Pi Desktop)
WARNINGs:
	If you are using Raspberry Pi 3, you need to fix UART (serial) once. Otherwise, it won't work with Sabertooths. See instrucitons below:
	//Instruction to turn off serial

	Run at startup instruction:
		$ sudo etc/profile
		Add to the end of profile: "sudo python3 /Pi/main.py"
		Save profile: Ctrl + X -> Y -> Enter
		Reboot Pi: $ sudo reboot

