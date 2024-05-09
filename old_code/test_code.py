import lumix_control as lc
from muselsl import list_muses, record_direct
import datetime
import time

muses = list_muses()

IP = "192.168.54.1" #IP of camera
control = lc.CameraControl(IP)
UDP_PORT = 5111

control.start_camera_control()
control.video_record_start()

SAVE_PATH = r"C:\Users\enesy\Videos\Brain Battle\21-12-23\Muse Recording Sessions\recording.csv"

if not muses:
    print("No muses")
else:
    muse_start_time = record_direct(5, muses[0]["address"], SAVE_PATH)
