import numpy as np
from pycromanager import Acquisition, multi_d_acquisition_events, Core
from pycromanager import start_headless
from pylab import *

def devTest():
    print("This is a test")
    core = Core()

    core.load_system_configuration(base.MM_CONFIG)
    #core.initialize_all_devices()
    #core.load_device("Core", "Camera",  "400BSI_V2")
    #core.set_camera_device("V1.0")
    core.snap_image()

    duration = 2
    framerate = 10
    num_time_points = duration * framerate


def record():
    with Acquisition(directory=base.SAVE_DIR) as acq:
        events = multi_d_acquisition_events(num_time_points=10)
        acq.acquire(events)

def headless():
    start_headless(base.MM_DIR, base.MM_CONFIG, timeout=5000)
    core = Core()

def snap()




