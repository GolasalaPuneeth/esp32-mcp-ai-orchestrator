from abc import ABC, abstractmethod
from fastmcp import FastMCP
from fastmcp.tools import tool
import json

light = FastMCP("Light Controller")

class LightDoc(ABC):
    """Abstract interface defining standard lighting capabilities."""
    
    @abstractmethod
    async def turn_on_light(self, switch: bool) -> bool:
        """
        Turn the physical light ON or OFF.
        
        Args:
            switch (bool): True to turn the light ON, False to turn it OFF.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_status(self) -> str:
        """Retrieve the current operational state of the light system."""
        raise NotImplementedError


class Light(LightDoc):
    
    @tool()  # Attach metadata for programmatic tool registration
    async def turn_on_light(self, switch: bool) -> bool:
        # Your hardware execution logic here (e.g., MQTT publish)
        return True

    @tool()
    async def get_status(self) -> str:
        status_data = {
            "status": "online",
            "led_state": "ON"
        }
        return json.dumps(status_data, indent=2)
