from camera_control import SonyControl, LumixControl, GoProControl
from time import sleep
import time
import threading
import logging
import asyncio
from muselsl import muse

# Create control objects.
sony_control = SonyControl()
sony_control.set_camera_url("http://10.0.0.1:10000/sony/camera")
lumix_control = LumixControl("192.168.235.129")

logging.getLogger().setLevel(logging.INFO)

go_control1 = GoProControl()
go_control2 = GoProControl()

device_list = asyncio.run(GoProControl.search_device())

if len(device_list) > 0:
    asyncio.run(go_control1.connect(device_list.popitem()[1]))
    asyncio.run(go_control2.connect(device_list.popitem()[1]))

def run_camera(control: GoProControl):
    asyncio.run(control.start_shutter())
    print(f"{control._name} started recording at {time.time()}")
    sleep(2)
    asyncio.run(control.stop_shutter())

# Take picture command
def lumix_take_video():
    lumix_control.video_record_start()
    print(f"Lumix started recording at {time.time()}")
    sleep(2)
    lumix_control.video_record_stop()

# Take picture command
def sony_take_pic():
    print(f"Sony started recording at {time.time()}")
    sony_control.start_movie_recording()
    sleep(2)
    sony_control.stop_movie_recording()

# Create threads for each function
t1 = threading.Thread(target=lumix_take_video)
t2 = threading.Thread(target=run_camera, args=[go_control1])
t3 = threading.Thread(target=run_camera, args=[go_control2])
t4 = threading.Thread(target=sony_take_pic)

# Run the threads
t1.start()
t2.start()
t3.start()
t4.start()

# Join the threads when they are done.
t1.join()
t2.join()
t3.join()
t4.join()
