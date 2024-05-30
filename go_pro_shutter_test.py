from camera_control import GoProControl
import asyncio
from time import sleep
import logging
import threading
logging.getLogger().setLevel(logging.INFO)

control1 = GoProControl()
control2 = GoProControl()

device_list = asyncio.run(GoProControl.search_device())

if len(device_list) > 0:
    asyncio.run(control1.connect(device_list.popitem()[1]))
    asyncio.run(control2.connect(device_list.popitem()[1]))

def run_camera(control: GoProControl):
    asyncio.run(control.start_shutter())
    sleep(2)
    asyncio.run(control.stop_shutter())

thread1 = threading.Thread(target=run_camera, args=[control1])
thread2 = threading.Thread(target=run_camera, args=[control2])

thread1.start()
thread2.start()

thread1.join()
thread2.join()

asyncio.run(control1.disconnect())
asyncio.run(control2.disconnect())

