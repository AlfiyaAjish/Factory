

import os, ssl, json, asyncio
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from scripts.utils.websocket.websocket_manager import alert_clients

load_dotenv()
main_loop = asyncio.get_event_loop()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connected to MQTT broker")
        client.subscribe("factory/+/alerts")
    else:
        print(" Failed to connect:", rc)

def on_message(client, userdata, msg):
    try:
        alert = json.loads(msg.payload.decode())
        print("\n ALERT:")
        print(f"Machine: {alert['machine_id']}, Temp: {alert['message']}")

        if main_loop:
            asyncio.run_coroutine_threadsafe(alert_clients(alert), main_loop)
        else:
            print(" Event loop not set. Alert not sent to WebSocket.")

    except Exception as e:
        print(" Error processing alert:", e)

def run_alert_subscriber():
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    client.tls_set(os.getenv("CA_CERT_PATH"), tls_version=ssl.PROTOCOL_TLS)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")))
    client.loop_start()

if __name__ == "__main__":
    asyncio.set_event_loop(main_loop)
    run_alert_subscriber()
    main_loop.run_forever()
