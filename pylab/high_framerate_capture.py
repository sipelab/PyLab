from pymmcore_plus import CMMCorePlus
import numpy as np
import tifffile
import os
import time

MM_CONFIG = r'C:/dev/DyhanaCam.cfg'
# Initialize the Core
mmc = CMMCorePlus().instance()
mmc.loadSystemConfiguration(MM_CONFIG)

# Function to acquire and save images into a single TIFF stack
def acquire_images(num_frames, output_filepath):
    mmc.startContinuousSequenceAcquisition(0)
    time.sleep(1)  # Allow some time for the camera to start capturing images
    
    images = []
    for i in range(num_frames):
        while mmc.getRemainingImageCount() == 0:
            time.sleep(0.01)  # Wait for images to be available
            
        if mmc.getRemainingImageCount() > 0 or mmc.isSequenceRunning():
            image = mmc.popNextImage()
            images.append(image)
    
    mmc.stopSequenceAcquisition()
    
    # Save images to a single TIFF stack
    tifffile.imwrite(output_filepath, np.array(images), imagej=True)

# Define parameters
num_frames = 100  # Number of frames to acquire
output_folder = r'C:/dev/sipefield/devOutput/'
output_filepath = os.path.join(output_folder, 'launchpy.tiff')

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Perform acquisition
acquire_images(num_frames, output_filepath)
