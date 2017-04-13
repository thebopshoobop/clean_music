"""Quick script to clean up music directories"""

import os
import os.path as op
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
    formatted = []
    the_ending = []
    extras = []
    numbers = Counter()
    empties = []

    for root, dirs, files in os.walk(directory):
        # Only check leaf folders
        if not dirs:
            # Missing album artwork
            if 'albumart.jpg' not in files:
                no_art.append(root)
            # Folders ending with ' 1'
            if re.search(r' 1$', root):
                if not re.search(r'vol\.|volume', root, re.I):
                    one_ending.append(root)
            # Disk mispelling
            if re.search(r'disk', root, re.I):
                disk.append(root)
            # Disc not capitalized or without a '(' before and a ' ' after
            if (
                    re.search(r'\(disc\ \d{1,2}\)', root)
                    or re.search(r'[^\(]disc', root, re.I)
                    or re.search(r'disc[^\ ]', root, re.I)
            ):
                formatted.append(root)
            # Ending with the
            if re.search(r'the$', root, re.I):
                the_ending.append(root)
            # Multiple dis[ck]s
            if len(re.findall(r'disc|disk', root, re.I)) > 1:
                extras.append(root)
            # Single disc albums with disc tags
            if re.search(r'\(disc|disk\ \d{1,2}\)', root, re.I):
                numbers[root[:-9]] += 1
            # No music
            dirsize = sum(op.getsize(op.join(root, name)) for name in files)
            if dirsize < size * 1000000:
                empties.append(root)

    click.secho('Missing arwork?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(no_art))

    click.secho('Ending with 1?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(one_ending))

    click.secho('Mispelling? -> disk:', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(disk))

    click.secho('Improper disc tag?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(formatted))

    click.secho('Ending with the?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(the_ending))

    click.secho('Multiple disc tags?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(extras))

    click.secho('Unneeded disc tags?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join([n for n, i in numbers.items() if i == 1]))

    click.secho('No music?', bg='blue', fg='white', bold=True)
    click.echo('\n'.join(empties))
