from azure.iot.device import IoTHubDeviceClient, Message
import time, random, json
from datetime import datetime

CONNECTION_STRING = "HostName=RideauSkatewayHub.azure-devices.net;DeviceId=FifthAveDevice;SharedAccessKey=IR6pScDm/jMAZPKgdAq2POsNe6YKBfZyVGnnATRTU9g="

def generate_data():
    return {
        "location": "Fifth Avenue",
        "iceThickness": random.randint(20, 35),
        "surfaceTemperature": random.randint(-10, 1),
        "snowAccumulation": random.randint(0, 15),
        "externalTemperature": random.randint(-15, 4),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

while True:
    payload = generate_data()
    message = Message(json.dumps(payload))
    message.content_encoding = "utf-8"
    message.content_type = "application/json"
    print("Sending:", payload)
    client.send_message(message)
    time.sleep(10)
