import tkinter as tk
from tkinter import messagebox

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
        self.camera_status.set("Connected")
        messagebox.showinfo("Info", "Camera Connected")

    def connect_eeg(self):
        eeg1_data = self.eeg1_data.get()
        eeg2_data = self.eeg2_data.get()
        if eeg1_data and eeg2_data:
            self.eeg_status.set("Connected")
            messagebox.showinfo("Info", f"EEG Connected with data: EEG1={eeg1_data}, EEG2={eeg2_data}")
        else:
            messagebox.showwarning("Warning", "Please enter data for both EEG1 and EEG2")

    def start_recording(self):
        if self.camera_status.get() == "Connected" and self.eeg_status.get() == "Connected":
            messagebox.showinfo("Info", "Recording Started")
        else:
            messagebox.showwarning("Warning", "Please connect both Camera and EEG before recording")

    def stop_recording(self):
        if self.camera_status.get() == "Connected" and self.eeg_status.get() == "Connected":
            messagebox.showinfo("Info", "Recording Stopped")
        else:
            messagebox.showwarning("Warning", "Recording is not in progress or devices are not connected")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
