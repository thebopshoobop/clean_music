"""Quick script to clean up music directories"""

import os
import os.path as op
import re
from collections import Counter
from shutil import rmtree

import click


def check_dir(directory, size):
    """Check the given directory for formatting problems."""

    all_discs = []
    disc_tags = Counter()
    results = {
        'art': {'label': 'Missing arwork?', 'dirs': []},
        'one': {'label': 'Ending with 1?', 'dirs': []},
        'disk': {'label': 'Mispelling? -> disk:', 'dirs': []},
        'format': {'label': 'Improper disc tag?', 'dirs': []},
        'the': {'label': 'Ending with the?', 'dirs': []},
        'extra': {'label': 'Multiple disc tags?', 'dirs': []},
        'single': {'label': 'Unneeded disc tags?', 'dirs': []},
        'empty': {'label': 'No music?', 'dirs': []},
    }

    for root, dirs, files in os.walk(directory):
        # Only check leaf directories
        if not dirs:
            # Missing album artwork
            if 'albumart.jpg' not in files:
                results['art']['dirs'].append(root)
            # Folders ending with ' 1'
            if re.search(r' 1$', root):
                if not re.search(r'vol\.|volume', root, re.I):
                    results['one']['dirs'].append(root)
            # Disk mispelling
            if re.search(r'disk', root, re.I):
                results['disk']['dirs'].append(root)
            # Disc not capitalized or without a '(' before and a ' ' after
            if (
                    re.search(r'\(disc\ \d{1,2}\)', root)
                    or re.search(r'[^\(]disc', root, re.I)
                    or re.search(r'disc[^\ ]', root, re.I)
            ):
                results['format']['dirs'].append(root)
            # Ending with the
            if re.search(r'the$', root, re.I):
                results['the']['dirs'].append(root)
            # Multiple dis[ck]s
            if len(re.findall(r'disc|disk', root, re.I)) > 1:
                results['extra']['dirs'].append(root)
            # Single disc albums with disc tags
            if re.search(r'\(disc\ \d\)$', root, re.I):
                all_discs.append(root)
                disc_tags[root[:-9]] += 1
            # No music
            dirsize = sum(op.getsize(op.join(root, name)) for name in files)
            if dirsize < size * 1000000:
                results['empty']['dirs'].append(root)

    results['single']['dirs'] = [n for n in all_discs
                                 if disc_tags[n[:-9]] == 1]

    return results


def display(label, dirs):
    """Given a label and a list of directories, display them."""
    click.secho(label, bg='blue', fg='white', bold=True)
    click.echo('\n'.join(sorted(dirs)))


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

    results = check_dir(directory, size)

    if not remove:
        for _, result in results.items():
            display(result['label'], result['dirs'])
    else:
        display(results['empty']['label'], results['empty']['dirs'])

        while True:
            click.secho('Delete directories? [y/n]', bg='red', fg='white',
                        bold=True)
            response = click.getchar()
            if response not in ['y', 'n']:
                click.echo('Warning: Invalid Input')
            elif response == 'y':
                for path in results['empty']['dirs']:
                    rmtree(path)
                break
            else:
                break
