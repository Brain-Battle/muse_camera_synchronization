from .camera_control.lumix_control import LumixControl

from .connection import Connection

class LumixConnection(Connection):
    def __init__(self, IP: str):
        self.IP = IP

    def connect(self):
        self.control = LumixControl(self.IP)
        self.control.start_camera_control()
        return self

    def start_recording(self):
        self.control.video_record_start()
        return self

    def stop_recording(self):
        self.control.video_record_stop()
        return self