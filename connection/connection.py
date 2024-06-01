from abc import ABC, abstractmethod

class Connection(ABC):
    """Base class for all connections
    """
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def start_recording(self):
        pass
    
    @abstractmethod
    def stop_recording(self):
        pass