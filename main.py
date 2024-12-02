import json
from paho.mqtt import client as mqtt
import os
import sys
from dotenv import load_dotenv
import uuid

load_dotenv(".env")

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
CLIENT_ID = f"WinterSupplement-{uuid.uuid4()}"

def calculate_winter_supplement(data):
    result = {
        "id": data["id"],
        "isEligible": data["familyUnitInPayForDecember"],
        "baseAmount": 0.0,
        "childrenAmount": 0.0,
        "supplementAmount": 0.0
    }
    if result["isEligible"]:
        if data["familyComposition"] == "single":
            result["baseAmount"] = 60.0
        elif data["familyComposition"] == "couple":
            result["baseAmount"] = 120.0

        result["childrenAmount"] = 20.0 * data["numberOfChildren"]
        result["supplementAmount"] = result["baseAmount"] + result["childrenAmount"]
    return result

def new_client(MQTT_TOPIC_ID) -> mqtt:
    MQTT_INPUT_TOPIC = f"BRE/calculateWinterSupplementInput/{MQTT_TOPIC_ID}"
    MQTT_OUTPUT_TOPIC = f"BRE/calculateWinterSupplementOutput/{MQTT_TOPIC_ID}"

    def on_message(client, userdata, message):
        print("Received message on topic:", message.topic)
        input_data = json.loads(message.payload.decode())
        print("Input data:", input_data)
        output_data = calculate_winter_supplement(input_data)
        client.publish(MQTT_OUTPUT_TOPIC, json.dumps(output_data))
        print("Published output data:", json.dumps(output_data))

    def on_connect(client, usedata, flags, rc, prop):
        print(f"Connection result code: {rc}")
        client.subscribe(MQTT_INPUT_TOPIC)
        print(f"Subscribed to topic: {MQTT_INPUT_TOPIC}")

    client = mqtt.Client(client_id=CLIENT_ID,
                        clean_session=True,
                        callback_api_version=
                            mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.on_connect = on_connect
    return client

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: MQTT topic ID must be provided as an argument.")
        sys.exit(1)
    
    MQTT_TOPIC_ID = sys.argv[1]
    try:
        client = new_client(MQTT_TOPIC_ID)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"Connected to {MQTT_BROKER} on port {MQTT_PORT}")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        sys.exit(1)

    try:
        print("Starting MQTT Client")
        client.loop_forever()
    except KeyboardInterrupt:
        print("Closing MQTT Client Connection")
        client.disconnect()
