#!/bin/sh
#launcher.sh
#This file will remove any folder whose name is RMCRobot in its current folder, then pull a brand new one from git.

sudo rm -rf RMCRobot
git clone git://github.com/HieuNguyen202/RMCRobot.git
#sudo python3 RMCRobot/Pi/Pi/Pi.py

