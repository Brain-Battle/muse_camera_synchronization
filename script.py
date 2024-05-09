import numpy as np
import pandas as pd
import os
from time import time, strftime, gmtime
from muselsl.stream import find_muse
from muselsl import backends
from muselsl.muse import Muse
from lumix_control import CameraControl

"""
    This is a modified version of the record_direct function that ships with muselsl.
    
    It adds camera functions on it which allows to start the cameras and Muse device
    at the same time.
"""
def start_recording(duration,
                  address,
                  filename=None,
                  backend='auto',
                  interface=None,
                  name=None):
    if backend == 'bluemuse':
        raise (NotImplementedError(
            'Direct record not supported with BlueMuse backend. Use record after starting stream instead.'
        ))

    if not address:
        found_muse = find_muse(name, backend)
        if not found_muse:
            print('Muse could not be found')
            return
        else:
            address = found_muse['address']
            name = found_muse['name']
        print('Connecting to %s : %s...' % (name if name else 'Muse', address))

    if not filename:
        filename = os.path.join(
            os.getcwd(),
            ("recording_%s.csv" % strftime("%Y-%m-%d-%H.%M.%S", gmtime())))

    eeg_samples = []
    timestamps = []

    def save_eeg(new_samples, new_timestamps):
        eeg_samples.append(new_samples)
        timestamps.append(new_timestamps)

    IP = "192.168.54.1" # IP of camera
    control = CameraControl(IP)
    UDP_PORT = 5111

    control.start_camera_control()

    muse = Muse(address, save_eeg, backend=backend)

    muse.connect()
    
    control.video_record_start()
    video_init = time()
    muse.start()
    t_init = time()

    print('Start video recording at time t= %.3f' % video_init)
    print('Start recording at time t=%.3f' % t_init)

    while (time() - t_init) < duration:
        try:
            backends.sleep(1)
        except KeyboardInterrupt:
            break

    muse.stop()
    control.video_record_stop()
    muse.disconnect()

    timestamps = np.concatenate(timestamps)
    eeg_samples = np.concatenate(eeg_samples, 1).T
    recording = pd.DataFrame(
        data=eeg_samples, columns=['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX'])

    recording['timestamps'] = timestamps

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    recording.to_csv(filename, float_format='%.3f')
    print('Done - wrote file: ' + filename + '.')
    print('Time difference between Muse and Video: ', t_init - video_init)
