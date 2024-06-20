"""
pylab base module.

This is the principal module of the pylab project.

"""

# example constant variable
NAME = "pylab"
SAVE_DIR = r'C:/dev/micro-manager_acq'
DEVTEST_DIR = r'C:/dev/micro-manager_acq/devtest'
SAVE_NAME = r'Acquisition_test'
MM_DIR = r'C:/Program Files/Micro-Manager-2.0'
MM_CONFIG = r'C:/Users/SIPE_LAB/Desktop/240620_config_devJG.cfg'

def launchCamera():
    """
    Launch the camera GUI.
    """
    print("Launching camera GUI...")

def launchWidefield():
    """
    Launch the widefield GUI.
    """
    print("Launching widefield GUI...")
    