from abc import ABC, abstractmethod
from fastmcp.tools import tool
from datetime import datetime
from AppUtils import MqttTool
import json



class LightDoc(ABC):
    """Abstract interface defining standard lighting capabilities."""
    
    @abstractmethod
    async def turn_control_light(self, switch: bool) -> bool:
        """
        Turn the physical light ON or OFF.
        
        Args:
            switch (bool): True to turn the light ON, False to turn it OFF.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def blink_light(self, times: int) -> bool:
        """
        Blink the physical light a specified number of times.
        
        Args:
            times (int): Number of times to cycle the blink.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_status(self) -> str:
        """Retrieve the current operational state of the light system."""
        raise NotImplementedError


class Light(LightDoc):
    def __init__(self):
        self.mqtt = MqttTool("mosquitto_mqtt", 1883)

    async def __aenter__(self):
        try:
            await self.mqtt.connect()
            return self

        except Exception:
            await self.mqtt.disconnect()
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.mqtt.disconnect()

    @tool()  
    async def turn_control_light(self, switch: bool) -> bool:
        if switch:
            return await self.mqtt.publish_command("ON")
        return await self.mqtt.publish_command("OFF")

    @tool()
    async def get_status(self) -> str:
        """Report whether the MQTT connection is available."""
        if self.mqtt.client is None:
            return "disconnected"
        return "connected"

    @tool()
    async def blink_light(self, times: int) -> bool:
        """Blink the light by alternating OFF and ON commands."""
        if times < 1:
            return False

        for _ in range(times):
            if not await self.mqtt.publish_command("ON"):
                return False
            if not await self.mqtt.publish_command("OFF"):
                return False
        return True