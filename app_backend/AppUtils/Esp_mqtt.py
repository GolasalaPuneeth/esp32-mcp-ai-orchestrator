import aiomqtt
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

pub_tpk = os.getenv('TOPIC_PUB')
ack_tpk = os.getenv('TOPIC_ACK')

async def send_mqtt_command(
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
                await client.subscribe(ack_tpk)
                await client.publish(pub_tpk, payload=payload)

                async for message in client.messages:
                    if message.topic.matches(ack_tpk):
                        return message.payload.decode(errors="replace")
    except TimeoutError:
        return "Device not reachable"
    except aiomqtt.MqttError as error:
        print("Device Not reachabe",error)
        return "Device not reachable"

    return "Device not reachable"