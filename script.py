import sony_control as sc
import lumix_control as lc
from time import sleep
import threading

sony_control = sc.SonyControl()
sony_control.set_camera_url("http://10.0.0.1:10000/sony/camera")

lumix_control = lc.LumixControl("192.168.9.129")

def lumix_take_pic():
    print(lumix_control.capture_photo().text)

def sony_take_pic():
    print(sony_control.take_picture().text)

t1 = threading.Thread(target=lumix_take_pic)
t2 = threading.Thread(target=sony_take_pic)

t1.start()
t2.start()

t1.join()
t2.join()
