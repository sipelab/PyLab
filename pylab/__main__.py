"""Entry point for pylab."""

from pylab.cli import main  # pragma: no cover
import click


'''
This is the client terminal command line interface

The client terminal commands are:

'''

@click.group()
def cli():
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

if __name__ == "__main__":  # pragma: no cover
    cli()


