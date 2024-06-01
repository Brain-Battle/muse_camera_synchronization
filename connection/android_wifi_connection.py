import socket
from .connection import Connection

class SocketConnection(Connection):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None

    def connect(self):
        """Establish a connection to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            print(f"Connected to {self.ip}:{self.port}")
        except socket.error as e:
            print(f"Error connecting to {self.ip}:{self.port} - {e}")
        return self

    def _send_byte(self, byte):
        """Send a single byte to the server."""
        try:
            self.socket.sendall(byte)
            print(f"Sent byte: {byte}")
        except socket.error as e:
            print(f"Error sending byte: {e}")

    def start_recording(self):
        self._send_byte(b'\1')
        return self

    def stop_recording(self):
        self._send_byte(b'\0')
        try:
            if self.socket:
                self.socket.close()
                print("Connection closed")
        except socket.error as e:
            print(f"Error closing the connection: {e}")
        return self