"""Entry point for pylab."""

from pylab.cli import main  # pragma: no cover
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



if __name__ == "__main__":  # pragma: no cover
    cli()


