from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import logging
import json
from datetime import datetime

app = Flask(__name__)

BROKER_URL = "broker"  # Docker Compose 서비스 이름 사용
BROKER_PORT = 1883

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

logging.basicConfig(level=logging.DEBUG)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    logging.debug(f"Received message: {msg.topic} {message}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER_URL, BROKER_PORT, 60)
mqtt_client.loop_start()

@app.route('/publish', methods=['POST'])
def publish_message():
    content = request.json
    message = content.get('messageText')
    chat_room_no = content.get('chatRoomNo')
    member_no = content.get('memberNo')
    message_date = content.get('messageDate')
    nickname = content.get('nickname')
    if message and chat_room_no and member_no and message_date:
        payload = {
            "messageText": message,
            "chatRoomNo": chat_room_no,
            "memberNo": member_no,
            "messageDate": message_date,
            "nickname": nickname
        }
        topic = f"chat/messages/{chat_room_no}"
        logging.debug(f"Publishing message to {topic}: {payload}")
        mqtt_client.publish(topic, json.dumps(payload))
        return jsonify({"status": "Message sent"}), 200
    else:
        return jsonify({"error": "Invalid data provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
