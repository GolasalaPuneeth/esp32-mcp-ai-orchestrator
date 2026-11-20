import asyncio
import json
import sys
import aiomqtt

class MqttTool:
    def __init__(self,broker:str,port:int):
        self.broker = broker
        self.port = port
        self.timeout = 3.0
        self.light_topic = "esp/light"
        self.light_ack = "esp/ack"
        self.light_on_load = json.dumps({"light": "ON"})
        self.light_off_load = json.dumps({"light": "OFF"})

    