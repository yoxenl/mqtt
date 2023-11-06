import paho.mqtt.client as mqtt
from random import randint, uniform
import time

# Connecting to MQTT Broker
mqttBroker = "mqtt.eclipseproject.io"

# Creating a client with the name "Temperature_Inside"
client = mqtt.Client("Number")

# Connects the client to our broker
client.connect(mqttBroker)

def inRange(number1):
    pass

while True:
    randNumber = randint(50)
    client.publish =("number", randNumber)
    print("Just published " + str(randNumber) + " to Topic number")
    time.sleep(1)

