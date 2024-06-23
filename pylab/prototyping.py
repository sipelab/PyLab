# import matlab.engine  

#   #The start_matlab function returns a Python object eng which enables you to pass data 
#     # and call functions executed by MATLAB. Background=True starts the engine asynchronously.
#     future = matlab.engine.start_matlab(background=True)
#     eng = future.result()
#     s = eng.genpath('C:/Users/SIPE_LAB/Desktop/desktop/WidefieldImager-master')
#     eng.addpath(s, nargout=0)
#     #eng.cd(r'C:/Users/SIPE_LAB/Desktop/desktop/WidefieldImager-master/WidefieldImager', nargout=0)
#     #eng.addpath('C:/Users/SIPE_LAB/Desktop/desktop/WidefieldImager-master/WidefieldImager')

#     eng.WidefieldImager(nargout=0)

# import serial.tools.list_ports
# import requests
# import serial.tools.list_ports

# def list_serial_ports():
#     """
#     List all available serial ports on the system
#     """
#     # Get a list of all available serial ports
#     ports = serial.tools.list_ports.comports()
    
#     # Check if there are any ports available
#     if not ports:
#         print("No serial ports found.")
#         return
    
#     # Print details of each available serial port
#     for port in ports:
#         print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")

# if __name__ == "__main__":
#     list_serial_ports()




# def download_usb_ids():
#     """
#     Download the USB IDs file from the internet resources 
#     """
#     url = "http://www.linux-usb.org/usb.ids"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.text
#     else:
#         print("Failed to download USB IDs")
#         return None

# def parse_usb_ids(usb_ids_content):
#     """
#     Parse the USB IDs file and return a dictionary of vendor IDs and product IDs
#     """

#     vendor_ids = {}
#     current_vendor_id = ""
#     for line in usb_ids_content.splitlines():
#         if not line or line.startswith("#") or line.startswith("\t\t"):
#             continue
#         if line.startswith("\t"):
#             product_id, product_name = line.strip().split(" ", 1)
#             vendor_ids[current_vendor_id]["products"][product_id] = product_name
#         else:
#             vendor_id, vendor_name = line.split(" ", 1)
#             current_vendor_id = vendor_id
#             vendor_ids[vendor_id] = {"name": vendor_name, "products": {}}
#     return vendor_ids

# def identify_device(vendor_id, product_id, usb_ids):
#     """
#     Identify the vendor and product of a USB device using the USB IDs file
#     """

#     vendor = usb_ids.get(vendor_id, {}).get("name", "Unknown Vendor")
#     product = usb_ids.get(vendor_id, {}).get("products", {}).get(product_id, "Unknown Product")
#     return vendor, product

# def list_serial_ports(usb_ids):
    
#     ports = serial.tools.list_ports.comports()
#     if not ports:
#         print("No serial ports found.")
#         return
#     for port in ports:
#         hwid_parts = port.hwid.split()
#         vid_pid = [part for part in hwid_parts if part.startswith("VID:PID=")]
#         if vid_pid:
#             vid, pid = vid_pid[0].replace("VID:PID=", "").split(":")
#             vendor, product = identify_device(vid, pid, usb_ids)
#             print(f"Device: {port.device}, Description: {port.description}, Vendor: {vendor}, Product: {product}")
#         else:
#             print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")

# if __name__ == "__main__":
#     usb_ids_content = download_usb_ids()
#     if usb_ids_content:
#         usb_ids = parse_usb_ids(usb_ids_content)
#         list_serial_ports(usb_ids)


import numpy as np
import matplotlib.pyplot as plt
from pycromanager import Core

MM_CONFIG = r'C:/Users/SIPE_LAB/Desktop/240620_config_devJG.cfg'
def launch_live_feed():
    core = Core()  # Get the core MicroManager object

    # Set up the camera for continuous acquisition
    core.load_system_configuration(MM_CONFIG)
    core.start_continuous_sequence_acquisition(1)  # 1 ms interval between images

    plt.ion()  # Enable interactive mode for live updates
    fig, ax = plt.subplots()  # Create a figure and axes for plotting
    image = np.zeros((512, 512))  # Placeholder for the first image
    im = ax.imshow(image, cmap='gray')  # Display the image

    try:
        while True:
            if core.get_remaining_image_count() > 0:  # Check if there are images to retrieve
                tagged_image = core.get_last_tagged_image()  # Get the next image
                image = np.reshape(tagged_image.pix, newshape=[tagged_image.tags['Height'], tagged_image.tags['Width']])
                im.set_data(image)  # Update the displayed image
                plt.draw()
                plt.pause(0.001)  # Short pause to allow GUI to update
            else:
                plt.pause(0.005)  # Wait a bit before checking for new images again
    except KeyboardInterrupt:
        # Stop acquisition when the user interrupts (e.g., by closing the plot or pressing Ctrl+C)
        core.stop_continuous_sequence_acquisition()
        plt.ioff()  # Turn off interactive mode
        plt.show()  # Keep the window open until explicitly closed

if __name__ == "__main__":
    launch_live_feed()