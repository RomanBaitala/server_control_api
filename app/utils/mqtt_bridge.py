import json
import paho.mqtt.client as mqtt
from app.bll.services import metric_service
from app.schemas import MetricCreate
from app.config.ext import db

def start_mqtt_listener(app):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(client, userdata, flags, rc, properties=None):
        print(f"Connected to MQTT Broker with code {rc}")
        client.subscribe("servers/+/metrics")

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
                    memory_usage=metric_in.memory_usage
                )
                print(f"Metrics saved for server {server_id}")
            except Exception as e:
                print(f"Error processing MQTT message: {e}")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    
    client.loop_start()