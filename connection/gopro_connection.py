from .connection import Connection
from .camera_control import GoProControl
import asyncio

class GoProConnection(Connection):
    device_list = asyncio.run(GoProControl.search_device())
    def __init__(self):
        self.control = GoProControl()
    
    def connect(self):
        asyncio.run(self.control.connect(GoProConnection.device_list.popitem()[1]))
        return self
    
    def start_recording(self):
        asyncio.run(self.control.start_shutter())
        return self
    
    def stop_recording(self):
        asyncio.run(self.control.stop_shutter())
        return self

    @classmethod
    def refresh(clf):
        clf.device_list = asyncio.run(GoProControl.search_device())