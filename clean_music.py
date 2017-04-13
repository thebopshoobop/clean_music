"""Quick script to clean up music directories"""

import os
import re
from collections import Counter

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

    no_art = []
    one_ending = []
    disk = []
    parens = []
    the_ending = []
    extras = []
    disc_numbers = Counter()
    empties = []

    for root, dirs, files in os.walk(directory):
        # Only check leaf folders
        if not dirs:
            # Missing album artwork
            if 'albumart.jpg' not in files:
                no_art.append(root)
            # Folders ending with ' 1'
            if re.search(r' 1$', root):
                one_ending.append(root)
            # Disk mispelling
            if re.search(r'disk', root, re.I):
                disk.append(root)
            # Disc without a '(' before and a ' ' after
            if (re.search(r'[^\(]disc', root, re.I)
                    or re.search(r'disc[^\ ]', root, re.I)):
                parens.append(root)
            # Ending with the
            if re.search(r'the$', root, re.I):
                the_ending.append(root)
            # Multiple dis[ck]s
            if len(re.findall(r'disc|disk', root, re.I)) > 1:
                extras.append(root)
            # Single disc albums with disc tags
            if re.search(r'\(disc|disk\ \d{1,2}\)', root, re.I):
                disc_numbers[root[:-9]] += 1
            # No music
            if ('albumart.jpg' in files and len(files) < 2) or not files:
                empties.append(root)
