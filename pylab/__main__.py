"""Entry point for pylab."""

#from pylab.cli import main  # pragma: no cover
import click

'''
This is the client terminal command line interface

The client terminal commands are:
'''

@click.group()
def cli():
    """PyLabs Command Line Interface"""
    pass

@cli.command()
#@click.option('--count', default=1, help='frame acquisitions')
def devtest():
    from pylab.camera import devTest
    devTest()

@cli.command()
def record():
    """
    Record a widefield acquisition.
    """
    from pylab.camera import record
    record()

### Utility commands for querying serial ports and USB IDs ###
@cli.command()
def get_devices():
    """Download USB IDs and list all serial ports."""
    from .utils import download_usb_ids, parse_usb_ids, list_serial_ports

    usb_ids_content = download_usb_ids()
    if usb_ids_content:
        usb_ids = parse_usb_ids(usb_ids_content)
        list_serial_ports(usb_ids)
    else:
        click.echo("Failed to download USB IDs.")

### NI-DAQ commands ###
from .utils import list_nidaq_devices, test_nidaq_connection, read_analog_input

@click.group()
def cli():
    """PyLab NI-DAQ Interface"""
    pass

@click.command()
def list_devices():
    """List all connected NI-DAQ devices."""
    devices = list_nidaq_devices()
    click.echo("\n".join(devices))

@click.command()
@click.argument('device_name')
def test_connection(device_name):
    """Test connection to a specified NI-DAQ device."""
    if test_nidaq_connection(device_name):
        click.echo(f"Successfully connected to {device_name}.")
    else:
        click.echo(f"Failed to connect to {device_name}.")

@click.command()
@click.argument('device_name')
def read_input(device_name):
    """Read a single analog input from the device."""
    value = read_analog_input(device_name)
    click.echo(f"Analog input value: {value}")

cli.add_command(list_devices)
cli.add_command(test_connection)
cli.add_command(read_input)

if __name__ == "__main__":  # pragma: no cover
    cli()


