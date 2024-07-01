import numpy as np
import tifffile
import os
from datetime import datetime, timedelta
from pymmcore_plus import CMMCorePlus
from qtpy.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLineEdit, QFormLayout, QLabel, QApplication
import nidaqmx
import time
import sys

SAVE_DIR = r'C:/dev/sipefield/devOutput'
MM_CONFIG = r'C:/dev/DyhanaCam.cfg'
FPS = 60  # Default FPS
DURATION = 50  # Default duration in seconds

mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration(MM_CONFIG)

# Initialize a list to store frames
frames = []

# Function to save frames as a TIFF stack with timestamps
def save_tiff_stack(frames, save_dir, protocol, subject_id, session_id):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    anat_dir = os.path.join(save_dir, f"{protocol}-{subject_id}", f"ses-{session_id}", "anat")
    os.makedirs(anat_dir, exist_ok=True)
    filename = os.path.join(anat_dir, f"sub-{subject_id}_ses-{session_id}_T1w_{timestamp}.tiff")
    tifffile.imwrite(filename, np.array(frames))
    print(f"Saved TIFF stack: {filename}")

# Function to start continuous acquisition
def start_continuous_acquisition(fps, duration):
    interval = 1 / fps
    end_time = datetime.now() + timedelta(seconds=duration)
    
    # Send the trigger signal when acquisition starts
    trigger(True)
    
    while datetime.now() < end_time:
        mmc.snapImage()
        image = mmc.getImage()
        frames.append(image)
        print(f"Captured frame: {len(frames)}")

        time.sleep(interval)
    
    # Send the trigger signal off when acquisition is complete
    trigger(False)
    
    # Save the collected frames as a TIFF stack
    save_tiff_stack(frames, SAVE_DIR, 'protocol', 'subject_id', 'session_id')

def trigger(state):
    # Function to send a high (TRUE) signal out of NIDAQ
    def send_trigger_signal():
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('Dev2/port0/line0')  # Hardware dependent value; check the NIDAQ device for the correct port and line
            task.do_channels.add_do_chan('Dev2/port0/line1')  # Hardware dependent value; check the NIDAQ device for the correct port and line
            task.write([True, True])
            print("Signal High from Dev2 on both lines")

    # Function to send a low (FALSE) signal out of NIDAQ
    def trigger_signal_off():
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('Dev2/port0/line0')
            task.do_channels.add_do_chan('Dev2/port0/line1')
            task.write([False, False])
            print("Signal Low from Dev2 on both lines")

    if state:
        send_trigger_signal()
    else:
        trigger_signal_off()

# Custom widget class for Napari
class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        
        # Form layout for parameters
        self.form_layout = QFormLayout()
        
        self.save_dir_input = QLineEdit(SAVE_DIR)
        self.fps_input = QLineEdit(str(FPS))
        self.duration_input = QLineEdit(str(DURATION))
        
        self.form_layout.addRow('Save Directory:', self.save_dir_input)
        self.form_layout.addRow('FPS:', self.fps_input)
        self.form_layout.addRow('Duration (seconds):', self.duration_input)
        
        self.layout.addLayout(self.form_layout)
        
        # Start Acquisition button
        self.button = QPushButton("Start Acquisition")
        self.button.clicked.connect(self.start_acquisition_with_params)
        self.layout.addWidget(self.button)
    
    def start_acquisition_with_params(self):
        global SAVE_DIR, FPS, DURATION
        SAVE_DIR = self.save_dir_input.text()
        FPS = int(self.fps_input.text())
        DURATION = int(self.duration_input.text())
        start_continuous_acquisition(FPS, DURATION)

# Function to start the application with the custom widget
def start_app():
    app = QApplication(sys.argv)
    main_window = QWidget()
    layout = QVBoxLayout(main_window)
    layout.addWidget(MyWidget())
    main_window.setLayout(layout)
    main_window.setWindowTitle("Continuous Acquisition")
    main_window.show()
    sys.exit(app.exec_())

# Launch the application with the custom widget
if __name__ == "__main__":
    start_app()
