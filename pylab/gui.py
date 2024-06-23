import tkinter as tk
from tkinter import messagebox
from utils import list_nidaq_devices, read_analog_input

def read_input_gui():
    device_name = device_entry.get()
    try:
        value = read_analog_input(device_name)
        messagebox.showinfo("Read Analog Input", f"Value: {value}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Nidaq Interface")

tk.Label(app, text="Device Name:").pack()
device_entry = tk.Entry(app)
device_entry.pack()

read_button = tk.Button(app, text="Read Analog Input", command=read_input_gui)
read_button.pack()

app.mainloop()