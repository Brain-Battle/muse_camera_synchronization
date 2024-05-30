from camera_control import SonyControl, LumixControl
from time import sleep
import threading

# Create control objects.
sony_control = SonyControl()
sony_control.set_camera_url("http://10.0.0.1:10000/sony/camera")
lumix_control = LumixControl("192.168.9.129")

# Take picture command
def lumix_take_pic():
    print(lumix_control.capture_photo().text)

# Take picture command
def sony_take_pic():
    print(sony_control.take_picture().text)

# Create threads for each function
t1 = threading.Thread(target=lumix_take_pic)
t2 = threading.Thread(target=sony_take_pic)

# Run the threads
t1.start()
t2.start()

# Join the threads when they are done.
t1.join()
t2.join()
