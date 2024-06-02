from muselsl.stream import find_muse
from muselsl import backends
from muselsl.muse import Muse
from time import time, strftime, gmtime
import os
import numpy as np
import pandas as pd
from .connection import Connection

class MuseConnection(Connection):
    def __init__(self, name: str,):
        self.name = name

    def connect(self):
        found_muse = find_muse(self.name, 'auto')
        if not found_muse:
            print('Muse could not be found')
            return  
        else:
            self.address = found_muse['address']
            self.name = found_muse['name']
            print('Connecting to %s : %s...' % (self.name if self.name else 'Muse', self.address))
        self.filename = os.path.join(os.getcwd(),
            (f"recording_{self.name}_%s.csv" % strftime("%Y-%m-%d-%H.%M.%S", gmtime())))
        self.eeg_samples = []
        self.timestamps = []
        def save_eeg(new_samples, new_timestamps):
            self.eeg_samples.append(new_samples)
            self.timestamps.append(new_timestamps)
        self.muse = Muse(self.address, save_eeg, backend='auto')
        self.muse.connect()
        return self

    def start_recording(self):
        self.muse.start()
        return self

    def stop_recording(self):
        self.muse.disconnect()
        timestamps = np.concatenate(self.timestamps)
        eeg_samples = np.concatenate(self.eeg_samples, 1).T
        recording = pd.DataFrame(
            data=eeg_samples, columns=['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX'])
        recording['timestamps'] = timestamps
        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        recording.to_csv(self.filename, float_format='%.3f')
        print('Done - wrote file: ' + self.filename + '.')
        return self
