import time, json, argparse, random, os
import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv
# from .constants.app_constants import BASE_URL

load_dotenv()

def register(machine_id, line):
    machine_info = {
        "machine_id": machine_id,
        "line": line,
        "location": "Factory-A",
        "operator": "John Doe"
    }
    try:
        res = requests.post("http://localhost:8009/machine/register/", json=machine_info)
        print(res.status_code, res.json())
    except Exception as e:
        print(" Failed to register machine:", e)

def simulate(machine_id, line):
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    client.tls_set(os.getenv("CA_CERT_PATH"))
    client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")))

    while True:
        payload = {
            "machine_id": machine_id,
            "line": line,
            "temperature": round(random.uniform(60, 100), 2),
            "units_produced": random.randint(10, 50)
        }
        topic = f"factory/{line}/{machine_id}"
        client.publish(topic, json.dumps(payload),retain=True)
        print("Sent:", payload)
        time.sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--line", required=True)
    args = parser.parse_args()

    register(args.id, args.line)
    simulate(args.id, args.line)
