# This fork ain't being worked on anymore. Go [here](https://github.com/aptgetmoo/moobot) for the good good

# moobot

moobot is a shitty discord bot that allows people to pay respects.

```
[12:35 AM] apt-get moo: f
[12:35 AM] moobot: apt-get moo pays their respects
```

now maybe won't crash every 0.00001 seconds

## prereqs

* python ~~3.4 or~~ 3.5
* virtualenv
* pip

(dropped support for python3.4 because I'm too lazy)

## install

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

I'm not currently on the discord server that interacts with moobot the most, so...

If you want me to:

* add moobot to your server
* fix this sorry mess
* shout at me for something else

you can join moobot's discord server. The link is [https://discord.gg/QDJYvTz](https://discord.gg/QDJYvTz).

