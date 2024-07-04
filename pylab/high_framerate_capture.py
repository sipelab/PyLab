from pymmcore_plus import CMMCorePlus
import numpy as np
import tifffile
import os
import time
from napari import Viewer, run
from qtpy.QtWidgets import QPushButton, QVBoxLayout, QWidget, QProgressBar

MM_CONFIG = r'C:/dev/DyhanaCam.cfg'

# Initialize the Core
mmc = CMMCorePlus().instance()
mmc.loadSystemConfiguration(MM_CONFIG)

def sanity_check(mmc):
    """
    Perform a sanity check to ensure that the Core is properly
    initialized and that the camera is connected. 

    This function lists: 
    - the loaded devices
    - configuration groups
    - current MMCore configuration settings 
    - camera settings.

    """
    print("Sanity Check:")
    print("=============")
    
    # ==== List all devices loaded by Micro-Manager ==== #
    devices = mmc.getLoadedDevices()
    print("Loaded Devices:")
    for device in devices:
        print(f" - {device}: {mmc.getDeviceDescription(device)}")
    
    # ==== Display configuration groups ==== #
    config_groups = mmc.getAvailableConfigGroups()
    print("\nConfiguration Groups:")
    for group in config_groups:
        print(f" - {group}")
        configs = mmc.getAvailableConfigs(group)
        for config in configs:
            print(f"    - {config}")
    
    # ==== Display current configuration ==== #
    print("\nCurrent Configuration:")
    # Get the current configuration settings for each group
    for group in config_groups:
        print(f" - {group}: {mmc.getCurrentConfig(group)}")
    
    # ==== Display camera settings ==== #
    camera_device = mmc.getCameraDevice()
    if camera_device:
        print(f"\nCamera Device: {camera_device}")
        print(f" - Exposure: {mmc.getExposure()} ms")
        print(f" - Pixel Size: {mmc.getPixelSizeUm()} um")
    else:
        print("\nNo camera device found.")

    
    print("\nOther Information:")
    print(f" - Image Width: {mmc.getImageWidth()}")
    print(f" - Image Height: {mmc.getImageHeight()}")
    print(f" - Bit Depth: {mmc.getImageBitDepth()}")

sanity_check(mmc)

# Function to acquire and save images into a single TIFF stack and visualize in Napari
def acquire_images(num_frames, output_filepath, viewer, progress_bar):
    mmc.startContinuousSequenceAcquisition(0)
    time.sleep(1)  # Allow some time for the camera to start capturing images
    
    images = [] # TODO preallocate images[] with frame parameter
    layer = None
    for i in range(num_frames):
        while mmc.getRemainingImageCount() == 0:
            time.sleep(0.01)  # Wait for images to be available
            
        if mmc.getRemainingImageCount() > 0 or mmc.isSequenceRunning():
            image = mmc.popNextImage()
            images.append(image)
            if layer is None:
                # Initialize the live-view layer on the first image
                layer = viewer.add_image(image, name='Live View')
            else:
                layer.data = image  # Update the image layer with the new frame

            # Update progress bar
            progress_bar.setValue((i + 1) * 100 // num_frames)
    
    mmc.stopSequenceAcquisition()
    
    # Save images to a single TIFF stack
    tifffile.imwrite(output_filepath, np.array(images), imagej=True)

    # Load the final TIFF stack into the viewer
    viewer.add_image(np.array(images), name='Final Acquisition')

# Define parameters
num_frames = 100  # Number of frames to acquire
output_folder = r'C:/dev/sipefield/devOutput/'
output_filepath = os.path.join(output_folder, 'launchpy.tiff')

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Custom widget class for Napari
class AcquisitionWidget(QWidget):
    def __init__(self, viewer, parent=None):
        super().__init__(parent)
        
        self.viewer = viewer
        self.layout = QVBoxLayout(self)
        
        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)
        
        # Start Acquisition button
        self.start_button = QPushButton("Start Acquisition")
        self.start_button.clicked.connect(self.start_acquisition)
        self.layout.addWidget(self.start_button)
    
    def start_acquisition(self):
        acquire_images(num_frames, output_filepath, self.viewer, self.progress_bar)

# Function to start the Napari viewer with the custom widget
def start_napari_with_widget():
    viewer = Viewer()
    viewer.window.add_dock_widget(AcquisitionWidget(viewer), area='right')
    run()

# Launch Napari with the custom widget
if __name__ == "__main__":
    start_napari_with_widget()
