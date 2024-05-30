import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
import os
from time import time, strftime, gmtime
from muselsl.stream import find_muse
from muselsl import backends
from muselsl.muse import Muse
from camera_control.lumix_control import LumixControl

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Connection and Recording")
        instructions = (
            "Instructions:\n"
            "1) Turn on Bluetooth\n"
            "2) Connect to camera Wi-Fi\n"
            "3) Connect EEG\n"
            "4) Connect Camera\n"
            "5) Start recording\n"
            "6) Stop recording"
        )
        self.instructions_label = tk.Label(root, text=instructions, justify=tk.LEFT)
        self.instructions_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.camera_status_label = tk.Label(root, text="Camera Status:")
        self.camera_status_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.camera_status = tk.StringVar()
        self.camera_status.set("Not Connected")
        self.camera_status_entry = tk.Entry(root, textvariable=self.camera_status, state='readonly')
        self.camera_status_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.eeg_status_label = tk.Label(root, text="EEG Status:")
        self.eeg_status_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.eeg_status = tk.StringVar()
        self.eeg_status.set("Not Connected")
        self.eeg_status_entry = tk.Entry(root, textvariable=self.eeg_status, state='readonly')
        self.eeg_status_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.eeg1_label = tk.Label(root, text="EEG1 Data:")
        self.eeg1_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.eeg1_data = tk.StringVar()
        self.eeg1_entry = tk.Entry(root, textvariable=self.eeg1_data)
        self.eeg1_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.eeg2_label = tk.Label(root, text="EEG2 Data:")
        self.eeg2_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.eeg2_data = tk.StringVar()
        self.eeg2_entry = tk.Entry(root, textvariable=self.eeg2_data)
        self.eeg2_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.connect_camera_button = tk.Button(root, text="Connect Camera", command=self.connect_camera)
        self.connect_camera_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        self.connect_eeg_button = tk.Button(root, text="Connect EEG", command=self.connect_eeg)
        self.connect_eeg_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        self.start_recording_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_recording_button.grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')
        self.stop_recording_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_recording_button.grid(row=8, column=0, columnspan=2, pady=10, sticky='ew')

    def connect_camera(self):
        connect_cameras()
        self.camera_status.set("Connected")
        messagebox.showinfo("Info", "Camera Connected")

    def connect_eeg(self):
        eeg1_data = self.eeg1_data.get()
        eeg2_data = self.eeg2_data.get()
        if eeg1_data and eeg2_data:
            connect_EEG(filenames=["1.csv", "2.csv"], names=[eeg1_data, eeg2_data])
            self.eeg_status.set("Connected")
            messagebox.showinfo("Info", f"EEG Connected with data: EEG1={eeg1_data}, EEG2={eeg2_data}")
        else:
            messagebox.showwarning("Warning", "Please enter data for both EEG1 and EEG2")

    def start_recording(self):
        if self.camera_status.get() == "Connected" and self.eeg_status.get() == "Connected":
            start_data_recording()
            messagebox.showinfo("Info", "Recording Started")
        else:
            messagebox.showwarning("Warning", "Please connect both Camera and EEG before recording")

    def stop_recording(self):
        if self.camera_status.get() == "Connected" and self.eeg_status.get() == "Connected":
            stop_recording_data()
            messagebox.showinfo("Info", "Recording Stopped")
        else:
            messagebox.showwarning("Warning", "Recording is not in progress or devices are not connected")

eeg_samples = []
timestamps = []
muses = []
t_init = 0
video_init = 0
control = None

"""
    This is a modified version of the record_direct function that ships with muselsl.
    
    It adds camera functions on it which allows to start the cameras and Muse device
    at the same time.
"""

def connect_EEG(
            filenames=None,
            backend='auto',
            interface=None,
            names=None):
    global eeg_samples
    global timestamps
    global muses
    devices_number = len(names)
    addresses = [0 for i in range(devices_number)]
    if backend == 'bluemuse':
        raise (NotImplementedError(
            'Direct record not supported with BlueMuse backend. Use record after starting stream instead.'
        ))
    for device in range(devices_number):
        found_muse = find_muse(names[device], backend)
        if not found_muse:
            print('Muse could not be found')
            return
        else:
            addresses[i] = found_muse['address']
            names[i] = found_muse['name']
        print('Connecting to %s : %s...' % (name if name else 'Muse', address))
    for device in range(len(filenames)):
        filenames[device] = os.path.join(
            os.getcwd(),
            (f"recording{device}_%s.csv" % strftime("%Y-%m-%d-%H.%M.%S", gmtime())))
    eeg_samples = [[] for i in range(devices_number)]
    timestamps = [[] for i in range(devices_number)]
    muses = []
    for device in range(devices_number):
        def save_eeg(new_samples, new_timestamps):
            eeg_samples[device].append(new_samples)
            timestamps[device].append(new_timestamps)
        muses.append(Muse(addresses[device], save_eeg, backend=backend))
    for muse in muses:
        muse.connect()

def connect_cameras(IP="192.168.54.1",
            UDP_PORT=5111):
    global control
    control = LumixControl(IP)
    control.start_camera_control()

def start_data_recording():
    global muses
    global control
    global t_init
    global video_init

    control.video_record_start()
    video_init = time()
    for muse in muses:
        muse.start()
    t_init = time()
    print('Start video recording at time t= %.3f' % video_init)
    print('Start recording at time t=%.3f' % t_init)

def stop_data_recording():
    global eeg_samples
    global timestamps
    global muses
    global control
    global t_init
    global video_init
    for muse in muses:
        muse.stop()
    control.video_record_stop()
    for muse in muses:
        muse.disconnect()
    for device in len(muses):
        timestamps[device] = np.concatenate(timestamps[device])
        eeg_samples[device] = np.concatenate(eeg_samples[device], 1).T
        recording = pd.DataFrame(
            data=eeg_samples[device], columns=['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX'])
        recording['timestamps'] = timestamps[device]

        directory = os.path.dirname(filenames[device])
        if not os.path.exists(directory):
            os.makedirs(directory)

        recording.to_csv(filenames[device], float_format='%.3f')
        print('Done - wrote file: ' + filenames[device] + '.')
        print('Time difference between Muse and Video: ', t_init - video_init)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

