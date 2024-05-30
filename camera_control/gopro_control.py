from bleak import *
import asyncio
import logging
import re

class GoProRequest:
    """
        GoProRequest class to wrap all byte requests that is available
        within GoPro BLE API.

        All commands follow the format:
        [Length of following message, Command Type, Value Length, Value]
    """

    SHUTTER_ON = bytearray([3, 1, 1, 1])
    SHUTTER_OFF = bytearray([3, 1, 1, 0])

class GoProUuid:
    GOPRO_UUID_BASE = "b5f9{0}-aa8d-11e3-9046-0002a5d5c51b"
    COMMAND_REQUEST = GOPRO_UUID_BASE.format("0072")
    COMMAND_RESPONSE = GOPRO_UUID_BASE.format("0073")
    SETTINGS_REQUEST = GOPRO_UUID_BASE.format("0074")
    SETTINGS_RESPONSE = GOPRO_UUID_BASE.format("0075")
    QUERY_REQUEST = GOPRO_UUID_BASE.format("0076")
    QUERY_RESPONSE = GOPRO_UUID_BASE.format("0077")

class GoProControl:
    def __init__(self):
        self._device: BleakClient = None
        self._event: asyncio.Event = asyncio.Event()

    @staticmethod
    async def search_device() -> dict[str, BLEDevice]:
        devices: dict[str, BLEDevice] = {}

        token = re.compile(r"GoPro [A-Z0-9]{4}")

        logging.info(f"Discovering.")
        for device in await BleakScanner.discover(timeout=10):
            if device.name and token.match(device.name):
                logging.info(f"Found device: {device.name}")
                devices[device.name] = device
        
        return devices

    async def connect(self, device: BLEDevice) -> None:
        self._device = BleakClient(device)

        logging.info(f"Trying to connect to: {device.name}")
        try: 
            await self._device.connect(timeout=15)
        except TimeoutError:
            logging.warning(f"Could not connect to the device: {device.name}")

        try:
            logging.info(f"Pairing with: {device.name}")
            await self._device.pair()
        except NotImplementedError:
            pass

        if self._device.is_connected:
            logging.info(f"Device succesfully connected. Address: {self._device.address}")

    async def disconnect(self) -> None:
        if self._device != None:
            logging.info(f"Disconnecting from: {self._device.address}")
            if await self._device.disconnect():
                self._device = None

    async def _send_command_request(self, request: GoProRequest):
        request_uuid = GoProUuid.COMMAND_REQUEST
        await self._device.write_gatt_char(request_uuid, request, response=True)

    async def start_shutter(self):
        logging.info(f"Starting shutter for: {self._device.address}")
        await self._send_command_request(GoProRequest.SHUTTER_ON)

    async def stop_shutter(self):
        logging.info(f"Stopping shutter for: {self._device.address}")
        await self._send_command_request(GoProRequest.SHUTTER_OFF)