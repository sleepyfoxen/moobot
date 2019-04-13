# moobot

moobot is a discord bot that allows people to pay respects.

```
[12:35 AM] apt-get moo: f
[12:35 AM] moobot: apt-get moo pays their respects
```

i wrote it to be modular; each module provides some (usually joke) commands.

## prereqs

* `fortune`, `cowsay`
* python 3.5+
* virtualenv
* pip

(python 3.4 is no longer supported)

## install

These instructions are for python 3.5, but you can just replace 3.5 with newer versions of python.

**set up virtualenv**

`virtualenv -p $(which python3.5) .venv`

`source .venv/bin/activate`

**install dependencies**

`pip install -r requirements.txt`

**next, add your discord token in the config.py file.**

**then, run**

`python moobot.py`

### improvements if i had more time

* get better memes (difficult)
* use flask like decorator functions to specify the command / bot trigger and move all the logic out of `moobot.py`.

### warnings

a `Bot` is just a subclass of `discord.Client` (so moving to the `Bot` framework was pretty easily done).

if you use a self-compiled python, make sure that `sqlite-devel` or `libsqlite3-dev` (debian) is installed and `--enable-loadable-sqlite-extensions` is set (which may or may not be set by default if sqlite3-dev is already present)

