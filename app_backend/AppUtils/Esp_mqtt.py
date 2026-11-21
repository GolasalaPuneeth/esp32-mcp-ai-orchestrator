
import asyncio
import json
import aiomqtt


class MqttTool:

    def __init__(self, broker: str, port: int):
        self.broker = broker
        self.port = port
        self.timeout = 3.0
        self.command_topic = "esp/light"
        self.ack_topic = "esp/ack"
        self.client = None
        self.commands = {
            "ON": {"light": "ON"},
            "OFF": {"light": "OFF"}
        }

    # ----------------------------------
    # Connection Management
    # ----------------------------------

    async def connect(self):
        self.client = aiomqtt.Client(
            hostname=self.broker,
            port=self.port
        )
        await self.client.__aenter__()
        print("[MQTT] Connected successfully")

    async def disconnect(self):
        if self.client is not None:
            await self.client.__aexit__(None, None, None)
            self.client = None
            print("[MQTT] Disconnected")

    # ----------------------------------
    # ACK Listener
    # ----------------------------------

    async def receive_ack(self):
        async for message in self.client.messages:
            if str(message.topic) != self.ack_topic:
                continue
            payload = message.payload.decode()
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return {"raw": payload}
        return {}

    # ----------------------------------
    # Publish and Receive ACK
    # ----------------------------------

    async def publish_command(self, command: str):
        if self.client is None:
            raise RuntimeError("MQTT client is not connected")
        payload = json.dumps(self.commands[command])
        try:
            # Subscribe before publishing
            await self.client.subscribe(
                self.ack_topic,
                qos=1
            )

            # Start ACK listener
            ack_task = asyncio.create_task(
                self.receive_ack()
            )

            try:
                # Publish command
                await self.client.publish(
                    self.command_topic,
                    payload=payload,
                    qos=1
                )
                print(f"[MQTT] Published: {payload}")
                # Wait for ACK
                response = await asyncio.wait_for(
                    ack_task,
                    timeout=self.timeout
                )
                print(f"[MQTT] ACK: {response}")
                return response

            finally:
                if not ack_task.done():
                    ack_task.cancel()
                await asyncio.gather(
                    ack_task,
                    return_exceptions=True
                )

        except asyncio.TimeoutError:
            print("[MQTT] ACK timeout")
            return None

        except aiomqtt.MqttError as exc:
            print(f"[MQTT] Error: {exc}")
            return None

    # ----------------------------------
    # Light Operations
    # ----------------------------------

    # async def light_on(self):

    #     return await self.publish_command("ON")

    # async def light_off(self):

    #     return await self.publish_command("OFF")