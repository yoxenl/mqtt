import paho.mqtt.client as mqtt 
from random import randrange
import time

from dotenv import load_dotenv
import os
load_dotenv()

topic = os.environ["topic"]
broker_port = os.environ["broker_port"]
hostname = os.environ["hostname"]

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed to: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print("Published to topic " + msg.topic + " with the QoS of " + str(msg.qos) + ". Message recieved: " + msg.payload.decode())

# Produces a new number in range of the assigned number
def inRange(startNumber):
    numberRange = 10
    numberMin = startNumber - numberRange
    numberMax = startNumber + numberRange
    
    # Limits the number to be in range of our expected range
    if numberMin < rangeMin:
        numberMin = rangeMin
    if numberMax > rangeMax + 1:
        numberMax = rangeMax + 1

    randNumber = randrange(numberMin - 1, numberMax)
    return randNumber

# Generates a random number inside of the assigned range
rangeMin = 0
rangeMax = 50
randNumber = randrange(rangeMin, rangeMax)

# Creates a client
client = mqtt.Client()
# Defines client functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

# Establishes the connection to the broker
client.connect(hostname, int(broker_port), 60)
client.subscribe(topic)
client.loop_start()

running = True

while running:
    print("Welcome to the Robot Terminal")
    print("Here is how to use the program:")
    print("""
        Default speed is 25 and default direction is forward
        'r' = check the current pwm value, 's' = stop, 'e' = exit
        'f' = forward, 'b' = backward
        'l' = low, 'm' = medium, 'h' = high
        To run motor 1, type in f1
        Type any number to set the speed (0-100)
        """)
    response = input(": ")
    client.publish(topic, payload=response)