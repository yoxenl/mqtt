from gpiozero import Motor, PhaseEnableMotor
from time import sleep

motor = Motor(17, 18)
motor2 = PhaseEnableMotor(12, 5)
motor.forward()
sleep(5)
motor.stop()
sleep(2)
motor2.forward()
sleep(5)
motor2.stop()