from abc import ABC, abstractmethod
from fastmcp.tools import tool
from datetime import datetime
import json

# light = FastMCP("Light Controller")
DEVICE_STATUS = {
    "light_current_status":"off",
    "last_change": None
}

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
    
    @tool()  
    async def turn_on_light(self, switch: bool) -> bool:
        print("[get_status] ------> ",switch)
        DEVICE_STATUS["current_status"]="on"
        DEVICE_STATUS["last_change"]= datetime.now().isoformat()
        print(DEVICE_STATUS)
        return True

    @tool()
    async def get_status(self) -> str:
        print("[get_status] ------> ")
        return json.dumps(DEVICE_STATUS, indent=2)

    @tool()
    async def blink_light(self, times):
        print("[blink_light] ------> ",times)
        return True