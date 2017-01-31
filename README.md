# moobot

moobot is a shitty discord bot that allows people to pay respects.

```
[12:35 AM] apt-get moo: f
[12:35 AM] moobot: apt-get moo pays their respects
```

it also does some other that are mostly memes.


## prereqs

* `fortune`, `cowsay`
* python 3.5 or 3.6
* virtualenv
* pip

(python 3.4 is no longer supported)

## install

These instructions are for python 3.5, but you can just replace 3.5 with 3.6 for the newer version of python.

**set up virtualenv**

`virtualenv -p $(which python3.5) .venv`

`source .venv/bin/activate`

**install dependencies**

`pip install -r requirements.txt`

**next, add your discord token in the config.py file (you can also use username / password based auth, but it's not recommended).**

**then, run**

`python moobot.py`

:D

### things to make this slightly less shitty

* get better memes (difficult)
* use flask like decorator functions to specify the command / bot trigger and move all the logic out of `moobot.py`.

### warnings

discord.py is really hip and cool but unfortunately it doesn't document any of the `ext` framework. Luckily it's mostly self explanatory. Protip: a `Bot` is just a subclass of `discord.Client` (so moving to the `Bot` framework was pretty easily done).

Also, if you are cool enough to use a compiled python, make sure that `sqlite-devel` or `libsqlite3-dev` (debian) is installed and `--enable-loadable-sqlite-extensions` is set (which may or may not be set by default if sqlite dev is already present)


### shout at me

If you want to:

* add moobot to your server for some reason
* yell at me to fix this sorry mess
* shout at me for something else

you can join moobot's discord server. The link is [https://discord.gg/QDJYvTz](https://discord.gg/QDJYvTz).

