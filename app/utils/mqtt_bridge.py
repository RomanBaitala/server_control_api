import json
import paho.mqtt.client as mqtt
from app.bll.services import metric_service, server_service
from app.schemas import MetricCreate
from datetime import datetime, timezone

def start_mqtt_listener(app):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker successfully")
            client.subscribe("servers/+/metrics")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):
        with app.app_context():
            try:
                payload = json.loads(msg.payload)
                server_id = int(msg.topic.split('/')[1])
                
                payload['server_id'] = server_id
                metric_in = MetricCreate(**payload)

                metric_service.add_metric(
                    server_id=metric_in.server_id,
                    cpu_usage=metric_in.cpu_usage,
                    cpu_temperature=metric_in.cpu_temperature,
                    memory_usage=metric_in.memory_usage,
                    timestamp=datetime.now(timezone.utc)
                )

                server_service.mark_online(server_id)
                
                print(f"Metrics saved and status updated for server {server_id}")

            except Exception as e:
                print(f"Error processing MQTT message for topic {msg.topic}: {e}")

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("localhost", 1883, 60)
        client.loop_start()
    except Exception as e:
        print(f"Could not connect to MQTT Broker: {e}")