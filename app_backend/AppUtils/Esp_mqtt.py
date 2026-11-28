import aiomqtt
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def send_mqtt_command(
    top_pub: str,
    top_ack: str,
    payload: str,
) -> str:
    """Publish a command and wait up to 3 seconds for a response.

    Connects to the MQTT broker at localhost:1883, subscribes to ``top_ack``,
    and publishes ``payload`` to ``top_pub``. Returns the response payload if
    a message arrives on ``top_ack``; otherwise returns ``Device not reachable``.
    """
    try:
        async with asyncio.timeout(3):
            async with aiomqtt.Client(hostname="localhost", port=1883) as client:
                await client.subscribe(top_ack)
                await client.publish(top_pub, payload=payload)

                async for message in client.messages:
                    if message.topic.matches(top_ack):
                        return message.payload.decode(errors="replace")
    except TimeoutError:
        return "Device not reachable"
    except aiomqtt.MqttError as error:
        print("Device Not reachabe",error)
        return "Device not reachable"

    return "Device not reachable"