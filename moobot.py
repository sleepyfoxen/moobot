#!/usr/bin/env python
"""moobot
moobot is a shitty discord bot that helps people
pay their respects
"""

import discord
import asyncio

import sqlite3


client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('%s - %s' % (client.user.name, client.user.id))


@client.event
@asyncio.coroutine
def on_message(message):
    # should we use the username or the nickname?
    name = getattr(message.author, 'nick', None)
    if name is None:
        name = message.author.name


    if message.content == 'x' or message.content == 'f':
        # we do two things:
        # 1. we increment their respect tallies in sqlite
        # 2. we let everyone know how respectful they are

        u = (message.author.id,)

        c.execute('select * from respect where user=?', u)
        u_ = c.fetchone()
        if u_ is not None:

            c.execute('update respect set f = f + 1 where user=?', u)
            conn.commit()

        else:
            # add user to db
            c.execute('insert into respect values(?, 1)', u)
            conn.commit()

        yield from client.send_message(message.channel,
                                       name + ' pays their respects')


    elif message.content == 'respect':
        # we're asked for how much respect someone has
        u = (message.author.id,)
        c.execute('select * from respect where user=?', u)

        result = c.fetchone()
        if result is not None:
            # this user has respect
            yield from client.send_message(message.channel,
                                           '*%s*: %s respect' % (name, str(result[1])))

        else:
            # this user has not f'ed before
            yield from client.send_message(message.channel,
                                           '*%s*: no respect :(' % name)


# connect to the DB
conn = sqlite3.connect('respect.db')
c = conn.cursor()

c.execute('''create table if not exists respect
             (user text, f integer) ''')


client.run('token')
