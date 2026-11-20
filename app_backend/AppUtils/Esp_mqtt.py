
import asyncio
import json
import aiomqtt


class MqttTool:

    def __init__(self, broker: str, port: int):

        self.broker = broker
        self.port = port
        self.timeout = 3.0

        self.light_topic = "esp/light"
        self.light_ack = "esp/ack"

        self.light_on_load = json.dumps({"light": "ON"})
        self.light_off_load = json.dumps({"light": "OFF"})

        self.client = aiomqtt.Client(
            hostname=self.broker,
            port=self.port
        )

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def _wait_for_ack(self) -> dict:

        async for message in self.client.messages:
            if str(message.topic) == self.light_ack:
                raw = message.payload.decode()
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return {"raw": raw}
        return {}

    async def publish_and_wait_ack(
        self,
        pub_topic: str,
        ack_topic: str,
        command_payload: str,
        timeout: float = 3.0
    ):
        try:
            # Subscribe before publishing
            await self.client.subscribe(self.light_ack, qos=1)

            # Start ACK listener
            ack_task = asyncio.create_task(
                self._wait_for_ack()
            )

            try:
                # Publish command
                await self.client.publish(
                    pub_topic,
                    payload=command_payload,
                    qos=1
                )

                print(f"Published {command_payload} -> {pub_topic}")

                ack = await asyncio.wait_for(
                    ack_task,
                    timeout=timeout
                )

                print(f"Received ACK on {ack_topic}: {ack}")

                return ack

            except asyncio.TimeoutError:
                print(
                    f"Timed out after {timeout}s "
                    f"waiting for ACK on {ack_topic}"
                )
                return None

            finally:
                if not ack_task.done():
                    ack_task.cancel()

                await asyncio.gather(
                    ack_task,
                    return_exceptions=True
                )

        except aiomqtt.MqttError as exc:
            print(f"MQTT error: {exc}")
            return None

    async def light_on(self):

        return await self.publish_and_wait_ack(
            pub_topic=self.light_topic,
            ack_topic=self.light_ack,
            command_payload=self.light_on_load,
            timeout=self.timeout
        )

    async def light_off(self):

        return await self.publish_and_wait_ack(
            pub_topic=self.light_topic,
            ack_topic=self.light_ack,
            command_payload=self.light_off_load,
            timeout=self.timeout
        )


async def main():

    async with MqttTool("localhost", 1883) as mqtt:

        response = await mqtt.light_on()
        print("Response:", response)


if __name__ == "__main__":
    asyncio.run(main())
