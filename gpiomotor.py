import SBC_MotoDriver3_Lib as SBC
import RPi.GPIO as GPIO
from time import sleep
import sys

# Valid inputs are between 0-100 which is equvelent to 0-100% duty cycles in PWM
def setSpeed(speed):
    try:
        if 100 >= speed >= 0:
            p.ChangeDutyCycle(0)
            p.ChangeDutyCycle(speed)
        else: 
            print('Not a valid value, please enter a value between 0 - 100')
    except:
        print('Error, please enter an integer between 0 - 100')

def statusCheck():
    print(SBC.pwmStatus)

def forward():
    SBC.allOn(True, False)

def forward1():
    SBC.on(0)

def backward():
    SBC.allOn(False, True)

def stop():
    SBC.allOff()

def low()
    p.ChangeDutyCycle(0)
    p.ChangeDutyCycle(50)

def medium():
    p.ChangeDutyCycle(0)
    p.ChangeDutyCycle(25)

def high():
    p.ChangeDutyCycle(0)

def exitProgram():
    print('Exiting...')
    SBC.allOff()
    GPIO.cleanup()
    sys.exit(0)
    return

# Switch case
commands = {
    'r': statusCheck,
    'f': forward,
    'f1': forward1,
    'b': backward,
    's': stop,
    'l': low,
    'm': medium,
    'h': high,
    'e': exitProgram
}

pwmStart = 50
_oe_pin = 0x15
gpioPin = 17

while True:
    SBC.init(_oe_pin, gpioPin)
    SBC.enabled(Ture)
    SBC.begin()
    SBC.allOff()
    p = GPIO.PWM(gpioPin, 1500)
    p.start(pwmStart)

    print('''
        Default speed and direction is 50 and forward
        r = checks the pwm status, s = stop, e = exit program
        f = forward, b = backwards
        l = low, m = medium, h = high
        To run motor 1, f1
        Type any number between 0-100 to set a new speed
    ''')

    running = True

    while running:
        x = input()

        if x == 'e':
            exitProgram()

        try:
            int(x)
            setSpeed(x)

        except:

            try:
                x = x.lower()
                commadns[x]()
                
            except:
                print('Not a valid input, try again')

    break