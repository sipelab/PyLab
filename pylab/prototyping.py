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
#         list_serial_ports(usb_ids)0

import nidaqmx
from nidaqmx.constants import LineGrouping
import time

def generate_trigger_signal():
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(
            'Dev2/port0/line0',
            line_grouping=LineGrouping.CHAN_PER_LINE
        )
        task.do_channels.add_do_chan(
            'Dev2/port0/line1',
            line_grouping=LineGrouping.CHAN_PER_LINE
        )
        
        while True:
            # Generate a high signal on both lines
            task.write([True, True])
            print("Signal High from Dev2 on both lines")
            time.sleep(1)  # Adjust as necessary
            
            # Generate a low signal on both lines
            task.write([False, False])
            print("Signal Low from Dev2 on both lines")
            time.sleep(1)  # Adjust as necessary

if __name__ == "__main__":
    generate_trigger_signal()