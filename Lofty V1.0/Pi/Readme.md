# H1 Lofty Software - Pi
## Requirements:
1. Fix UART (see instruction)
2. Run at startup
## Fix UART instructions
	If you are using Raspberry Pi 3, you need to fix UART (serial) once. Otherwise, it won't work with Sabertooths. See instrucitons below:
	'''sudo raspi-config'''
	Disable serial (yes disable it)
	'''sudo nano /boot/config.txt'''
	Add “UART_enable =1” or “enable_uart=1” at the end of config.txt
## Run at startup instruction
	'''$ sudo etc/profile'''
	Add to the end of profile: "sudo python3 /Pi/main.py"
	Save profile: Ctrl + X -> Y -> Enter
	Reboot Pi: 
	'''$ sudo reboot'''
## Installation	
	Put this folder in the Raspberry Pi's Desktop
	Reboot
