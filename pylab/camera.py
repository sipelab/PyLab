import numpy as np
from pycromanager import Acquisition, multi_d_acquisition_events, Core
from pycromanager import start_headless
from matplotlib.pyplot import imshow
from pylab import base

def launch():
    print("Initializing Micro Manager Device configuration from config file..." + base.MM_CONFIG)
    # Initialize the core object for Micromanager API
    core = Core()
    # Load the system configuration file
    core.load_system_configuration(base.MM_CONFIG)


def record():
    with Acquisition(directory=base.SAVE_DIR) as acq:
        events = multi_d_acquisition_events(num_time_points=10)
        acq.acquire(events)


    
# def headless():
#     start_headless(base.MM_DIR, base.MM_CONFIG, timeout=5000)
#     core = Core()

# def snap():
#     core = Core()
#     core.snap_image()
#     image = core.get_image()
#     imshow(image)



