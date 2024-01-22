import sys
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
from pipefile import *

# get arguments from main.py
script_name = sys.argv[0]
encryption_key = (sys.argv[1:][0]).encode("utf-8")
channel = sys.argv[1:][1]


def encrypt_message(message):
    global encryption_key

    cipher_suite = Fernet(encryption_key)
    cipher_text = cipher_suite.encrypt(message.encode())

    return cipher_text


# open mqtt communication
client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 0)

while True:
    received_data = listen_file("result")
    client.publish(channel, encrypt_message(received_data))



