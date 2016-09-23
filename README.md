# moobot

moobot is a shitty discord bot that allows people to pay respects.

```
[12:35 AM] apt-get moo: f
[12:35 AM] moobot: apt-get moo pays their respects
```

now maybe won't crash every 0.00001 seconds

## prereqs

* python 3.4 or 3.5
* virtualenv
* pip

## install

**set up virtualenv**

`virtualenv -p $(which python3) .venv`

`source .venv/bin/activate`

**install dependencies**

`pip install -r requirements.txt`

**next, add your discord token in the moobot.py file (you can also use username / password based auth, but it's not recommended).**

**then, run**

`python moobot.py`

:D

### things to make this slightly less shitty

* get better memes (difficult)
* use flask like decorator functions to specify the command / bot trigger and move all the logic out of `moobot.py`.
