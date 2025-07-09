

import json
from datetime import datetime
from scripts.utils.mqtt.mqtt_client import create_mqtt_client
from scripts.utils.mongodb_utils import metrics_collection, is_machine_registered
from scripts.handler.celery.periodic_tasks  import check_and_alert

main_loop = None

def on_connect(client, userdata, flags, rc):
    print(" MQTT Subscriber Connected")
    client.subscribe("factory/+/+")

def on_message(client, userdata, msg):
    global main_loop
    try:
        data = json.loads(msg.payload.decode())
        machine_id = data["machine_id"]

        if not is_machine_registered(machine_id):
            print(f"Unregistered machine: {machine_id}")
            return

        data["timestamp"] = datetime.utcnow().isoformat()


        check_and_alert.delay(data)

        metrics_collection.insert_one(data)
        print(f" Stored metrics for {machine_id}")

    except Exception as e:
        print(" Error in MQTT on_message:", e)

def start_subscriber(loop):
    global main_loop
    main_loop = loop
    client = create_mqtt_client(on_connect, on_message)
    client.loop_start()
