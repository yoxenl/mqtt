import time
import paho.mqtt.client as mqtt

# from quizero import App, Text, PushButton
import sys

import SBC_MotoDriver3_Lib as SBC
import RPi.GPIO as GPIO

from dotenv import load_dotenv
import os
load_dotenv()

'''
def close_gui():
    sys.exit()

app = App(title = 'GUI Development')
message = Text(app, text = 'test GUI')
button1 = PushButton(app, text = 'START', width = '10', height = '3')
button2 = PushButton(app, text = 'STOP', width = '10', height = '3')
button3 = PushButton(app, command = close_gui, text = 'CLOSE', width = '10', height = '3')
'''

# Robot identifier
robotID = 0
ref = 'Robot' + robotID + ':'

_oe_pin = 0x15
gpio_pin = 17

maxSpeed = 100
speed = 25
minSpeed = 0

topic = os.environ['topic']
topic_reciever = os.environ['topic_reciever']
broker_port = os.environ['broker_port']
hostname = os.environ['hostname']

def on_connect(client, userdata, flags, rc):
    msg = 'Connection attempt returned ' + mqtt.connack_string(rc)
    sendOutput(msg)


def on_message(client, userdata, msg):
    msg = msg.payload.decode()
    message = 'Message recieved: ' + msg
    sendOutput(msg)
    readMsg(msg)

def readMsg(message):
    if message == 'e':
        exitProgram()
    
    if message == 'unsubscribe' or message == 'unsub':
        to_unsubscribe()
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
            msg = 'Not a valid input, try again\n' + str(e)
            sendOutput(msg)

    except Exception as e:
        sendOutput(str(e))

def to_unsubscribe():
    msg = 'Initiating to unsubscribe to topic ' + topic
    sendOutput(msg)

    try: 
        result = client.unsubscribe(topic)

        if result[0] == 0:
            msg = 'Successfully unsubscribed from topic ' + topic
            sendOutput(msg)

        else: 
            msg = 'Unsubscribing to topic ' + topic + ' failed'
            sendOutput(msg)

    except Exception as e:
        msg = 'Error on unsubscribing:\n' + str(e)
        sendOutput(msg)

def startMotor():
    SBC.init(_oe_pin, gpio_pin)
    SBC.enabled(True)
    SBC.begin()
    SBC.allOff()

def sendOutput(message):
    client.publish(topic_reciever, payload=ref + ' ' + message)

# Valid inputs are between 0-100, equivelent to 0-100% duty cycle in PWM
# 100 is however complete resistance
def setSpeed(speed):
    try:
        if maxSpeed >= speed >= minSpeed:
            p.ChangeDutyCycle(0)
            p.ChangeDutyCycle(speed)
    
        else:
            msg = f'Not a valid value, please entera value between {minSpeed} - {maxSpeed}'
            sendOutput(msg)

    except Exception as e:
        msg = 'Error, please enter an integer between 0 - 100\n' + str(e)
        sendOutput(msg)

def statusCheck():
    status = SBC.pwmStatus(0)
    msg = f'current PWM value: {status}'
    sendOutput(msg)

def forward():
    SBC.allOn(True, False)
    msg = 'Forward'
    sendOutput(msg)

def forward1():
    SBC.on(0)
    msg = 'Motor 1 forward'
    sendOutput(msg)

def backward():
    SBC.allOn(False, True)
    msg = 'Backward'
    sendOutput(msg)

def stop():
    SBC.allOff()
    msg = 'Stopping motors'
    sendOutput(msg)

def low():
    p.ChangeDutyCycle(0)
    p.ChangeDutyCycle(50)
    msg = 'Low'
    sendOutput(msg)

def medium():
    p.ChangeDutyCycle(0)
    p.ChangeDutyCycle(25)
    msg = 'Medium'
    sendOutput(msg)

def high():
    p.ChangeDutyCycle(0)
    msg = 'Low'
    sendOutput(msg)

def exitProgram():
    msg = 'Exiting...'
    sendOutput(msg)
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
p.start(speed)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(hostname, broker_port, 60)

client.subscribe(topic)
client.loop_forever()