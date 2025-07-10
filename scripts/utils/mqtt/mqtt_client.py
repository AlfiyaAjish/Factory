import os
import ssl
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

def create_mqtt_client(on_connect=None, on_message=None):
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    client.tls_set(os.getenv("CA_CERT_PATH"), tls_version=ssl.PROTOCOL_TLS)

    if on_connect:
        client.on_connect = on_connect
    if on_message:
        client.on_message = on_message

    client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")))
    return client
