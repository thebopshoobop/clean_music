# Clean your music (directories)

A quick and dirty script to discover all the misformatted music directories you've got crusting up your hard drive.

Uses the excellent [click](http://click.pocoo.org) cli library.

### What it does:

 * List borked directories:
   * no albumart.jpg
   * end with ' 1' (but not Vol. 1 or Volume 1)
   * disc mispelled disk
   * disc not capitalized or parenthesized
   * end with ' the'
   * multiple disc tags
   * unneeded disc tags
   * no actual music‽
 * Delete directories wthout music

### Install it!

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install click
$ pip install .
```

### Run it!

```
# Display all the gross from a different directory
$ clean_music -d /home/will/Music
# Specify a different no-music threshold (default 2MB)
$ clean_music 5
# Display and offer to remove no-music directories
$ clean_music -r
```
