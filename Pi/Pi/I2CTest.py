from Utility import *

arduinoController = I2C(7)

def main():
    i2cTest()
    print("Done sending data!")
def i2cTest():
    arduinoController.setMotorAddress(128)
    arduinoController.setArmAddress(129)
    arduinoController.setHandAddress(130)
    arduinoController.setArmHeight(20)
    arduinoController.setArmAngle(30)
    arduinoController.setHandAngle(40)
    arduinoController.setHandHeight(50)
    arduinoController.setArmHeightOffset(60)
    arduinoController.setHandHeightOffset(70)
    arduinoController.setHandAngleOffset(80)
    arduinoController.setMotorPower(90,120)
    arduinoController.setArmPower(100)
    arduinoController.setHandPower(110)
    arduinoController.stopMotor()
    arduinoController.stopArm()
    arduinoController.stopHand()
    arduinoController.setSabertoothAddresses(128,129,130)
if __name__ == "__main__":
        main()

