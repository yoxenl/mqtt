import time
import paho.mqtt.client as mqtt

# from quizero import App, Text, PushButton
import sys

import SBC_MotoDriver3_Lib as SBC
import RPi.GPIO as GPIO

from dotenv import load_dotenv
import os
load_dotenv()

"""
def close_gui():
    sys.exit()

app = App(title = "GUI Development")
message = Text(app, text = "test GUI")
button1 = PushButton(app, text = "START", width = "10", height = "3")
button2 = PushButton(app, text = "STOP", width = "10", height = "3")
button3 = PushButton(app, command = close_gui, text = "CLOSE", width = "10", height = "3")
"""

# Robot identifier
robotID = 0
ref = 'Robot' + robotID

_oe_pin = 0x15
gpio_pin = 17

topic = os.environ["topic"]
broker_port = os.environ["broker_port"]
hostname = os.environ["hostname"]

maxSpeed = 100
startSpeed = 50
minSpeed = 0

def on_connect(client, userdata, flags, rc):
    print("Connection attempt returned " + mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    msg = msg.payload.decode()
    print("Message recieved: " + msg)
    readMsg(msg)

def readMsg(message):
    if message == 'e':
        exitProgram()
    
    if message == 'unsubscribe' or message == 'unsub':
        to unsubscribe()
        return

    try:
        speed = int(message)
        setSpeed(speed)
        return

    except ValueError: 
        try: 
            message = message.lower()
            commands[message]()

        except Exception as e: 
            print('Not a valid input, try again\n' + str(e))

    except Exception as e:
        print(str(e))

def to_unsubscribe():
    print("Initiating to unsubscribe to topic " + topic)
    try: 
        result = client.unsubscribe(topic)
        if result[0] == 0:
            print("Successfully unsubscribed from topic " + topic)
        else: 
            print("Unsubscribing to topic " + topic + " failed")
    except Exception as e:
        print("Error on unsubscribing:\n" + str(e))

def startMotor():
    SBC.init(_oe_pin, gpio_pin)
    SBC.enabled(True)
    SBC.begin()
    SBC.allOff()

def setSpeed(speed):
    try:
        if maxSpeed >= speed >= minSpeed:
            p.ChangeDutyCycle(0)
            p.ChangeDutyCycle(speed)
    
        else:
            print(f'Not a valid value, please entera value between {minSpeed} - {maxSpeed}')

    except Exception as e:
        print('Error, please enter an integer between 0 - 100\n' + str(e))

def statusCheck():
    print(SBC.pwmStatus(0))

def forward():
    SBC.allOn(True, False)

def forward1():
    SBC.on(0)

def backward():
    SBC.allOn(False, True)

def stop():
    SBC.allOff()

def low():
    p.ChangeDutyCycle(0)
    p.ChangeDutyCycle(50)

def medium():
    p.ChangeDutyCycle(0)
    p.ChangeDutyCycle(25)

def high():
    p.ChangeDutyCycle(0)

def exitProgram():
    print('Exiting')
    SBC.allOff
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

def thisRobot(robotnumber):
    pass

startMotor()

p = GPIO.PWM(gpio_pin, 1500)
p.start(startSpeed)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(hostname, broker_port, 60)

client.subscribe(topic)
client.loop_forever()