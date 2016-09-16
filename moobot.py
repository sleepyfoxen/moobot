#!/usr/bin/env python
"""moobot
moobot is a shitty discord bot that helps people
pay their respects
"""

import discord
import asyncio

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('%s - %s' % (client.user.name, client.user.id))


@client.event
@asyncio.coroutine
def on_message(message):
    if message.content == 'x' or message.content == 'f':
        if hasattr(message.author, 'nick'):
            yield from client.send_message(message.channel, message.author.nick + ' pays their respects')


client.run('token')
