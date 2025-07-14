
from scripts.constants.app_constants import AppConstants
import json
from datetime import datetime
from scripts.utils.mqtt.mqtt_client import create_mqtt_client
from scripts.utils.mongodb_utils import metrics_collection, is_machine_registered
from scripts.utils.mongodb_utils import alerts_collection,metrics_collection,machines_collection
from scripts.utils.websocket.redis_pub import publish_alert_to_redis
import asyncio

# from scripts.handler.celery.periodic_tasks  import check_and_alert

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


        check_and_alert(data)

        metrics_collection.insert_one(data)
        print(f" Stored metrics for {machine_id}")

    except Exception as e:
        print(" Error in MQTT on_message:", e)


def check_and_alert(data: dict):
    try:
        temperature = data.get("temperature", 0)
        machine_id = data["machine_id"]

        machine = machines_collection.find_one({"machine_id": machine_id})

        base_temp = machine.get("base_temperature", AppConstants.ALERT_TEMP_THRESHOLD)

        if temperature > base_temp:
            alert = {
                "machine_id": machine_id,
                "line": data["line"],
                "message": f"High Temperature: {temperature}°C",
                "timestamp": data["timestamp"],
                "resolved": False
            }


            mqtt_client = create_mqtt_client()
            topic = f"factory/{machine_id}/alerts"
            mqtt_client.loop_start()
            mqtt_client.publish(topic, json.dumps(alert),retain=True)
            mqtt_client.loop_stop()

            publish_alert_to_redis(alert)


            alerts_collection.insert_one(alert)




            print(f" Alert published to MQTT Topic: {topic}")
        else:
            print(" Temperature normal")

    except Exception as e:
        print("task error:", e)



def start_subscriber(loop):
    global main_loop
    main_loop = loop
    client = create_mqtt_client(on_connect, on_message)
    client.loop_start()
