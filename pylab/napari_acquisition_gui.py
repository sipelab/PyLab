from pymmcore_plus import CMMCorePlus
import numpy as np
import tifffile
import os
from datetime import datetime
from napari import Viewer, run
from qtpy.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QFormLayout, QProgressBar
import nidaqmx


import time

SAVE_DIR = r'C:/dev/sipefield/devOutput'
SAVE_NAME = r'Acquisition_test'
MM_DIR = r'C:/Program Files/Micro-Manager-2.0'
MM_CONFIG = r'C:/dev/DyhanaCam.cfg'

mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration(MM_CONFIG)

# Initialize a list to store frames
frames = []

# Default parameters for file saving
save_dir = SAVE_DIR
protocol_id = "devTIFF"
subject_id = "001"
session_id = "01"
num_frames = 10
output_filepath = os.path.join(save_dir, 'high_framerate_prototyping.tiff')

# Function to save frames as a TIFF stack with timestamps
def save_tiff_stack(frames, save_dir, protocol, subject_id, session_id):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # get current timestamp
    anat_dir = os.path.join(save_dir, f"{protocol}-{subject_id}", f"ses-{session_id}", "anat")
    os.makedirs(anat_dir, exist_ok=True) # create the directory if it doesn't exist
    filename = os.path.join(anat_dir, f"sub-{subject_id}_ses-{session_id}_{timestamp}.tiff")
    tifffile.imwrite(filename, np.array(frames)) # save the TIFF stack
    print(f"Saved TIFF stack: {filename}")


def trigger_decorator(func):
    def wrapper():
        trigger(True)
        func()
        trigger(False)

class NIDAQ:
    '''
    Class to handle NI-DAQ operations for digital output. The class is used as a context manager to ensure proper initialization and cleanup of the NI-DAQ task. 
    The send_signal method is used to send a digital signal to the specified channels
    The trigger method is a convenience method to send a high signal followed by a low signal to the channels.
    
    Parameters:
    - device_name (str): Name of the NI-DAQ device (default: 'Dev2')
    - channels (list): List of channel names to use for digital output (default: ['port0/line0', 'port0/line1'])
    '''
    def __init__(self, device_name='Dev2', channels=None):
        self.device_name = device_name
        self.channels = channels if channels else ['port0/line0', 'port0/line1']
        self.task = None

    def __enter__(self):
        self.task = nidaqmx.Task()
        for channel in self.channels:
            full_channel_name = f'{self.device_name}/{channel}'
            self.task.do_channels.add_do_chan(full_channel_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
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



# Function to start the MDA sequence
def start_acquisition(viewer, progress_bar):
    
    mmc.startContinuousSequenceAcquisition(0)
    time.sleep(1)  # TODO: Allow some time for the camera to start capturing images ???
    trigger(True)

    images = []
    layer = None
    start_time = time.time()  # Start time of the acquisition
    for i in range(num_frames):
        while mmc.getRemainingImageCount() == 0:
            time.sleep(0.1)  # TODO: Wait for images to be available ???
            
        if mmc.getRemainingImageCount() > 0 or mmc.isSequenceRunning():
            # TODO: Insert frame timing function for testing
            image = mmc.popNextImage()
            images.append(image)
            if layer is None:
                # Initialize the live-view layer on the first image
                layer = viewer.add_image(image, name='Live View')
            else:
                layer.data = image  # Update the image layer with the new frame

            # Update progress bar
            progress_bar.setValue((i + 1) * 100 // num_frames)
    
    end_time = time.time()  # End time of the acquisition
    elapsed_time = end_time - start_time  # Total time taken for the acquisition
    framerate = num_frames / elapsed_time  # Calculate the average framerate
    
    mmc.stopSequenceAcquisition()
    trigger(False)
    
    print(f"Average framerate: {framerate} frames per second")
    
    # Save images to a single TIFF stack
    # tifffile.imwrite(output_filepath, np.array(images), imagej=True)
    save_tiff_stack(images, save_dir, protocol_id, subject_id, session_id)
    # Load the final TIFF stack into the viewer
    viewer.add_image(np.array(images), name='Final Acquisition')



# Custom widget class for Napari
class MyWidget(QWidget):
    def __init__(self, viewer, parent=None):
        super().__init__(parent)
        
        self.viewer = viewer
        self.layout = QVBoxLayout(self)
        
        # ==== Progress bar ==== #
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)

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
        start_acquisition(self.viewer, self.progress_bar)
        

    def test_trigger(self):
        with NIDAQ() as nidaq:
            nidaq.trigger(True)
            time.sleep(1)
            nidaq.trigger(False)


# Function to start Napari with the custom widget
def start_napari():
    print("Starting Sipefield Napari Acquisition Interface...")
    viewer = Viewer()
    # Activate live view
    viewer.window.add_plugin_dock_widget('napari-micromanager')
    viewer.window.add_dock_widget(MyWidget(viewer), area='right')
    run()

# Launch Napari with the custom widget
if __name__ == "__main__":
    start_napari()
