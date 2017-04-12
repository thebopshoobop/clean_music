"""Quick script to clean up music directories"""

import os

import click


@click.command()
def clean():
    """Quick script to clean up music directories"""

    click.echo(os.listdir('.'))
