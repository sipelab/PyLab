import serial.tools.list_ports
import requests
import serial.tools.list_ports


### Utility functions for querying serial ports and USB IDs ###


def list_serial_ports():
    """
    List all available serial ports on the system
    """
    # Get a list of all available serial ports
    ports = serial.tools.list_ports.comports()
    
    # Check if there are any ports available
    if not ports:
        print("No serial ports found.")
        return
    
    # Print details of each available serial port
    for port in ports:
        print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")

if __name__ == "__main__":
    list_serial_ports()


def download_usb_ids():
    """
    Download the USB IDs file from the internet resources 
    """
    url = "http://www.linux-usb.org/usb.ids"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to download USB IDs")
        return None

def parse_usb_ids(usb_ids_content):
    """
    Parse the USB IDs file and return a dictionary of vendor IDs and product IDs
    """

    vendor_ids = {}
    current_vendor_id = ""
    for line in usb_ids_content.splitlines():
        if not line or line.startswith("#") or line.startswith("\t\t"):
            continue
        if line.startswith("\t"):
            product_id, product_name = line.strip().split(" ", 1)
            vendor_ids[current_vendor_id]["products"][product_id] = product_name
        else:
            vendor_id, vendor_name = line.split(" ", 1)
            current_vendor_id = vendor_id
            vendor_ids[vendor_id] = {"name": vendor_name, "products": {}}
    return vendor_ids

def identify_device(vendor_id, product_id, usb_ids):
    """
    Identify the vendor and product of a USB device using the USB IDs file
    """

    vendor = usb_ids.get(vendor_id, {}).get("name", "Unknown Vendor")
    product = usb_ids.get(vendor_id, {}).get("products", {}).get(product_id, "Unknown Product")
    return vendor, product

def list_serial_ports(usb_ids):
    """
    List all available serial ports on the system and identify connected USB devices
    """
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
        return
    for port in ports:
        hwid_parts = port.hwid.split()
        vid_pid = [part for part in hwid_parts if part.startswith("VID:PID=")]
        if vid_pid:
            vid, pid = vid_pid[0].replace("VID:PID=", "").split(":")
            vendor, product = identify_device(vid, pid, usb_ids)
            print(f"Device: {port.device}, Description: {port.description}, Vendor: {vendor}, Product: {product}")
        else:
            print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")
