import time
import paho.mqtt.client as mqtt

from quizero import App, Text, PushButton
import sys

from dotenv import load_dotenv
import os
load_dotenv()

def close_gui():
    sys.exit()

app = App(title = "GUI Development")
message = Text(app, text = "test GUI")
button1 = PushButton(app, text = "START", width = "10", height = "3")
button2 = PushButton(app, text = "STOP", width = "10", height = "3")
button3 = PushButton(app, command = close_gui, text = "CLOSE", width = "10", height = "3")

topic = os.environ["topic"]
broker_port = os.environ["broker_port"]
hostname = os.environ["hostname"]

def on_connect(client, userdata, flags, rc):
    print("Connection attempt returned " + mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    msg = msg.payload.decode()
    print("Message recieved: " + msg)
    to_unsubscribe(msg)

def to_unsubscribe(message):
    if message == "stop":
        print("Initiating to unsubscribe to topic " + topic)
        try: 
            result = client.unsubscribe(topic)
            if result[0] == 0:
                print("Successfully unsubscribed from topic " + topic)
            else: 
                print("Unsubscribing to topic " + topic + " failed")
        except Exception as e:
            print("Error on unsubscribing:\n" + str(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(hostname, broker_port, 60)

client.subscribe(topic)
client.loop_forever()