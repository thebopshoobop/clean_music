"""Quick script to clean up music directories"""

import os

import click


@click.command()
@click.option(
    '-d', '--directory', default='.',
    help='Specify a directory, rather than using the current one'
)
@click.option(
    '-r', '--remove', is_flag=True,
    help='''Remove small directories rather than displaying info'''
)
@click.argument('size', default=2)
def clean(directory, remove, size):
    """Quick script to clean up music directories:
    * Displays improperly formatted directories
    * Displays directories that are too small to likely have any music (default
    2MB). You may specify a different maximum size.
    """
