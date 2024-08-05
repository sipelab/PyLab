from pymmcore_plus import CMMCorePlus
import numpy as np
import tifffile
import os
from datetime import datetime
from napari import Viewer, run
from qtpy.QtWidgets import QCheckBox, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QFormLayout, QProgressBar
import nidaqmx
import threading
import queue
from queue import Queue
import time
from tqdm import tqdm
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari

import time
import pandas as pd

#SAVE_DIR = r'C:/dev/sipefield/devOutput'
SAVE_NAME = r'Acquisition_test'
MM_DIR = r'C:/Program Files/Micro-Manager-2.0'
MM_CONFIG = r'C:/dev/ThorPupil.cfg'
NIDAQ_DEVICE = 'Dev1'
CHANNELS = ['port2/line0']
IO = 'input' # is the NIDAQ an INput or Output Device?

print("loading Micro-Manager CORE...")
mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration(MM_CONFIG)

# Default parameters for file saving
save_dir = r'F:/sbaskar/202407_SB_F31prelim_pupil'
protocol_id = "baseline"
subject_id = "devJG"
session_id = "01"
num_frames = 24000

###THREADING
frame_queue = Queue()
stop_event = threading.Event()
############

# Class to save frames as a TIFF stack with timestamps
class Output:
    def __init__(self, save_dir=save_dir, protocol=protocol_id, subject_id=subject_id, session_id=session_id):
        self.save_dir = save_dir
        self.protocol = protocol
        self.subject_id = subject_id
        self.session_id = session_id

    def save(self, frames):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # get current timestamp
        anat_dir = os.path.join(self.save_dir, f"{self.protocol}-{self.subject_id}", f"ses-{self.session_id}", "anat")
        os.makedirs(anat_dir, exist_ok=True) # create the directory if it doesn't exist
        filename = os.path.join(anat_dir, f"sub-{self.subject_id}_ses-{self.session_id}_{timestamp}.tiff")
        tifffile.imwrite(filename, np.array(frames)) # save the TIFF stack
        print(f"Saved TIFF stack: {filename}")

    def save_md(self, metadata):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # get current timestamp
        metadata_dir = os.path.join(save_dir, f"{self.protocol}-{self.subject_id}", f"ses-{self.session_id}", "metadata")
        os.makedirs(metadata_dir, exist_ok=True) # create the directory if it doesn't exist
        filename = os.path.join(metadata_dir, f"sub-{self.subject_id}_ses-{self.session_id}_{timestamp}.csv")
        df = pd.DataFrame(metadata)
        df.to_csv(filename, index=False) # save the metadata as a CSV file
        print(f"Saved metadata: {filename}")
    
    def create_dataframe(self, frames):
        df = pd.DataFrame(frames)
        return df
class NIDAQ:
    '''
    Class to handle NI-DAQ operations for digital output. The class is used as a context manager to ensure proper initialization and cleanup of the NI-DAQ task. 
    The send_signal method is used to send a digital signal to the specified channels
    The trigger method is a convenience method to send a high signal followed by a low signal to the channels.
    
    Parameters:
    - device_name (str): Name of the NI-DAQ device (default: 'Dev2')
    - channels (list): List of channel names to use for digital output (default: ['port0/line0', 'port0/line1'])
    '''
    def __init__(self, device_name=NIDAQ_DEVICE, channels=CHANNELS, io=IO):
        self.device_name = device_name
        self.channels = channels if channels else ['port0/line0', 'port0/line1']
        self.task = None
        self._io = io 

    def __enter__(self):
        """During With context, generate input or output channels according to parameter 'io' """
        self.task = nidaqmx.Task()
        if self._io == "input": # Create input channel(s)
            for channel in self.channels:
                full_channel_name = f'{self.device_name}/{channel}'
                self.task.di_channels.add_di_chan(full_channel_name)
            return self
        else: # Create output channel(s)
            for channel in self.channels:
                full_channel_name = f'{self.device_name}/{channel}'
                self.task.do_channels.add_do_chan(full_channel_name)
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the task() on exit"""
        if self.task:
            self.task.close()

    def send_signal(self, signal_values):
        if not self.task:
            raise RuntimeError("Task not initialized. Use 'with NIDAQ(...) as nidaq:' context.")
        self.task.write(signal_values)
        print(f"Signal {'High' if all(signal_values) else 'Low'} on {self.device_name} for channels {self.channels}")

    def trigger(self, state):
        signal_values = [state] * len(self.channels)
        self.send_signal(signal_values)
        
    def pulse(self, duration=1):
        self.trigger(True)
        time.sleep(duration)
        self.trigger(False)


class FrameSavingThread(threading.Thread):
    def __init__(self, frame_queue, stop_event, filename):
        super().__init__()
        self.frame_queue = frame_queue
        self.stop_event = stop_event
        self.filename = filename

    def run(self):
        with tifffile.TiffWriter(self.filename) as tiff:
            with tqdm(total=num_frames, desc='Saving Frames') as pbar:
                while not self.stop_event.is_set() or not self.frame_queue.empty():
                    try:
                        frame = self.frame_queue.get(timeout=1)

                        # Append the frame to the TIFF file

                        tiff.write(frame) 
                        self.frame_queue.task_done()
                        pbar.update(1)
                    except queue.Empty:
                        continue    
                pbar.clear


# Function to start the MDA sequence
def start_acquisition(viewer, wait_for_trigger):

    ###THREADING
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # get current timestamp
    anat_dir = os.path.join(save_dir, f"{protocol_id}-{subject_id}", f"ses-{session_id}", "anat")
    os.makedirs(anat_dir, exist_ok=True) # create the directory if it doesn't exist
    output_filename = os.path.join(anat_dir, f"sub-{subject_id}_ses-{session_id}_{timestamp}.tiff")

    saving_thread = FrameSavingThread(frame_queue, stop_event, output_filename)
    ############

    if wait_for_trigger:
        with NIDAQ() as nidaq:
            if nidaq._io == "output": 
                # reset NIDAQ output trigger state
                with NIDAQ() as nidaq:
                    nidaq.trigger(False)
            else:
                print("Waiting for trigger...")
                while not nidaq.task.read(): # While input signal is not True
                    time.sleep(0.1)
    
    saving_thread.start()

    print(time.ctime(time.time()), ' trigger received, starting acquisition')
    mmc.startContinuousSequenceAcquisition(0)
    time.sleep(1)  # Allow some time for the camera to start capturing images

    images = []
    metadata = []
    layer = None
    start_time = time.time()  # Start time of the acquisition
    for i in range(num_frames):
        while mmc.getRemainingImageCount() == 0:
            time.sleep(0.1) 
            
        if mmc.getRemainingImageCount() > 0 or mmc.isSequenceRunning():
            image = mmc.popNextImage()
            #images.append(image)
            frame_queue.put(image)
            #print("frame acquired")
            # if layer is None:
            #     # Initialize the live-view layer on the first image
            #     layer = viewer.add_image(image, name='Live View')
            # else:
            #     layer.data = image  # Update the image layer with the new frame

    
    mmc.stopSequenceAcquisition()

    end_time = time.time()  # End time of the acquisition
    elapsed_time = end_time - start_time  # Total time taken for the acquisition
    framerate = num_frames / elapsed_time  # Calculate the average framerate

    ###THREADING
    print("!!! Stopping thread")
    stop_event.set()
    print("!!! Joining threads")
    saving_thread.join()
    ############

    if wait_for_trigger:
        if nidaq._io == "output": 
        # reset NIDAQ output trigger state
            with NIDAQ() as nidaq:
                nidaq.trigger(False)
        
    print(f"started at ctime: {time.ctime(start_time)} with Average framerate: {framerate} frames per second") # TODO sort out possible 2 second process delay between trigger and acquisition
    
    # Save images to a single TIFF stack with associated metadata
    # acquisition = Output(save_dir, protocol_id, subject_id, session_id)
    # acquisition.save(images)
    # Load the final TIFF stack into the viewer
    # viewer.add_image(np.array(images), name='Final Acquisition') #2024-08-04 This line adds several minutes after saving


# Custom widget class for Napari
class MyWidget(QWidget):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = viewer
        self.layout = QVBoxLayout(self)
        self._trigger_mode = True
        
        # ==== Progress bar ==== #
        # self.progress_bar = QProgressBar(self)
        # self.progress_bar.setMaximum(100)
        # self.layout.addWidget(self.progress_bar)

        # ==== Form layout for parameters ==== #
        self.form_layout = QFormLayout()
        
        # ==== Input fields for parameters ==== #
        self.save_dir_input = QLineEdit(save_dir)
        self.protocol_id_input = QLineEdit(protocol_id)
        self.subject_id_input = QLineEdit(subject_id)
        self.session_id_input = QLineEdit(session_id)
        self.num_frames_input = QLineEdit(str(num_frames))
        
        # === Labels for input fields === #
        self.form_layout.addRow('Save Directory:', self.save_dir_input)
        self.form_layout.addRow('Protocol ID:', self.protocol_id_input)
        self.form_layout.addRow('Subject ID:', self.subject_id_input)
        self.form_layout.addRow('Session ID:', self.session_id_input)
        self.form_layout.addRow('Number of Frames:', self.num_frames_input)
        self.layout.addLayout(self.form_layout) # Add the form layout to the main layout
        
        # === Checkbox for trigger mode === #
        self.checkbox = QCheckBox("Wait for Trigger")
        self.checkbox.setCheckState(True)
        self.checkbox.stateChanged.connect(self.set_trigger_mode)
        self.layout.addWidget(self.checkbox)
        
        # === Start Acquisition button === #
        self.button = QPushButton("Start Acquisition")
        self.button.clicked.connect(self.start_acquisition_with_params)
        self.layout.addWidget(self.button)

        # === Test Trigger button === #
        self.button = QPushButton("Test NiDAQ Trigger")
        self.button.clicked.connect(self.test_trigger)
        self.layout.addWidget(self.button) 
        
    def start_acquisition_with_params(self):
        global save_dir, protocol_id, subject_id, session_id, num_frames
        save_dir = self.save_dir_input.text()
        protocol_id = self.protocol_id_input.text()
        subject_id = self.subject_id_input.text()
        session_id = self.session_id_input.text()
        num_frames = int(self.num_frames_input.text())
        start_acquisition(self.viewer, self._trigger_mode)
        

    def test_trigger(self):
        with NIDAQ() as nidaq:
            nidaq.pulse()
            
    def set_trigger_mode(self, checked): # TODO have this change the acquisition trigger method
        if checked:
            self._trigger_mode = True
        else:
            self._trigger_mode = False


# Function to start Napari with the custom widget
def start_napari():
    
    print("launching interface...")
    viewer = Viewer()
    
    # Activate live view
    viewer.window.add_plugin_dock_widget('napari-micromanager')
    viewer.window.add_dock_widget(MyWidget(viewer), area='bottom')
    run()

# Launch Napari with the custom widget
if __name__ == "__main__":
    print("Starting Sipefield Napari Acquisition Interface...")
    start_napari()
