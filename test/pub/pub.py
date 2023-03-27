#!/usr/bin/env python3

import random
import time
import os

from paho.mqtt import client as mqtt_client


broker = os.environ.get('PUB_TARGET_IP')
port = int(os.environ.get('PUB_TARGET_PORT'))

username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')

client_id = f'mqttpub1'
topic = "Temperature"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        
        msg = f"{msg_count}. tempeture: {random.randint(200,800)/10}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    while True:
        time.sleep(1)
        try:
            client = connect_mqtt()
            client.loop_start()
            publish(client)
        except:
            print("Connection failed")

if __name__ == '__main__':
    run()