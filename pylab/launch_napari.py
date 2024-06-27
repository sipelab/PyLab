"""
jgronemeyer 2024
"""

import napari
from pymmcore_plus import CMMCorePlus
from qtpy.QtWidgets import QPushButton, QVBoxLayout, QWidget
import nidaqmx

# Custom Napari widget for button to start acquisition_with_trigger
class AcquisitionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.start_button = QPushButton('Start Acquisition', self)
        self.start_button.clicked.connect(start_acquisition)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

def daq_trigger_signal():
    '''Creates a trigger signal using a National Instruments DAQ device, sends a high (TRUE) and then low (FALSE) signal.'''
    # Function to send a high (TRUE) signal 
    def send_trigger_signal():
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(
                'Dev2/port0/line0') #Hardware dependent value; check the NIDAQ device for the correct port and line
            task.do_channels.add_do_chan(
                'Dev2/port0/line1') #Hardware dependent value; check the NIDAQ device for the correct port and line
            
            task.write([True, True])
            print("Signal High from Dev2 on both lines")

    # Function to send a low (FALSE) signal
    def trigger_signal_off():
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(
                'Dev2/port0/line0')
            task.do_channels.add_do_chan(
                'Dev2/port0/line1')
            
            task.write([False, False])
            print("Signal Low from Dev2 on both lines")


# Function to start acquisition and send trigger signal
def start_acquisition():
    mmc.startSequenceAcquisition(100, 0, True)  # Example acquisition parameters
    daq_trigger_signal()  # Send trigger signal


# Initialize the Napari viewer
viewer = napari.Viewer()

# Initialize widgets and plugins
acquisition_widget = AcquisitionWidget()
viewer.window.add_dock_widget(acquisition_widget, area='right')
dw, main_window = viewer.window.add_plugin_dock_widget("napari-micromanager") #load the napari-micromanager plugin

# quick way to access the same core instance as napari-micromanager
mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration('C:/Users/SIPE_LAB/Desktop/240620_config_devJG.cfg')  # Load your system configuration here
# Start the Napari event loop
napari.run()