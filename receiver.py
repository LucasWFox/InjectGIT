import sys
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
from pipefile import *

script_name = sys.argv[0]
encryption_key = (sys.argv[1:][0]).encode("utf-8")
channel = sys.argv[1:][1]


def decrypt_message(cipher_text):
    global encryption_key

    cipher_suite = Fernet(encryption_key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()

    return plain_text


def on_connect(client, userdata, flags, rc):
    global channel
    client.subscribe(channel)


def on_message(client, userdata, msg):
    message = decrypt_message(msg.payload.decode())
    post_file(message, "income")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 0)

client.loop_forever()

