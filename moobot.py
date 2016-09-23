"""moobot
moobot is a shitty discord bot that helps people
pay their respects
"""

import discord
import asyncio

import datetime
import re
import sqlite3

try:
    from fixed_karma import fixed
except ImportError as e:
    print("eh")

DEBUG = False

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('%s - %s' % (client.user.name, client.user.id))
    yield from client.change_status(game=discord.Game(name='moobot :D'))


@client.event
@asyncio.coroutine
def on_message(message):

    # should we use the username or the nickname?
    name = getattr(message.author, 'nick', None)
    if name is None:
        name = message.author.name


    if DEBUG and message.content.startswith('super_secret_message'):
        logs = yield from client.logs_from(message.channel, limit=10000)
        for log in logs:
            if log.content == 'f' or log.content == 'x':
                u = (log.author.id,)
                c.execute('select * from respect where user=?', u)
                u_ = c.fetchone()
                if u_ is not None:
                    c.execute('update respect set f = f + 1 where user=?', u)
                    conn.commit()
                else:
                    c.execute('insert into respect values(?, 1)', u)
                    conn.commit()

    elif DEBUG and message.content == 'harambe_memes':
        newest = datetime.datetime.now() - datetime.timedelta(days=1000)
        alt = False
        logs = yield from client.logs_from(message.channel, limit=1000)
        for log in logs:
            if 'harambe' in log.content and not log == message:
                if log.timestamp > newest:
                    newest = log.timestamp
                    alt = True

        if alt:

            result = c.execute('select * from harambe where channel=?', (message.channel.id,))
            channel = result.fetchone()

            if channel is not None:
                # don't mess with current data
                return
            else:
                # insert operation
                c.execute('insert into harambe values (?, "' + str(newest) + '")', (message.channel.id,))
                conn.commit()
                yield from client.send_message(message.channel, '[moobot debug]: %s' % str(newest))

    if len(message.content) == 1 and r.match(message.content) is not None:
        # we do two things:
        # 1. we increment their respect tallies in sqlite
        # 2. we let everyone know how respectful they are

        if message.author.id in fixed:
            # leet - don't change amount of stuffzies
            yield from client.send_message(message.channel,
                                           name + ' pays their respects')
            return

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


    elif message.content.lower() == 'respect':
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

    elif 'harambe' in message.content.lower():
        # need to reset the number of days since harambe was last mentioned
        # 1. check if the channel has ever crumbed before
        # -> either reset date to current time or start a counter
        channel_id = (message.channel.id,)

        c.execute('select * from harambe where channel=?', channel_id)
        result = c.fetchone()
        if result is not None:
            # previous channel
            # message.timestamp is a native datetime.datetime object
            # so in the database we are storing a serialised datetime.datetime object
            # (=> str(datetime.datetime), it's a string-encoded ISO-based date)
            d_last = datetime.datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S.%f')
            d_new = message.timestamp

            d = str(d_new)

            # update last in db
            c.execute('update harambe set last = "' + d + '" where channel=?',
                      channel_id)
            conn.commit()

            d_diff = d_new - d_last
            if d_diff.days >= 1:
                yield from client.send_message(message.channel,
                        'days since harambe was last mentioned: %s --> 0' % d_diff.days)

            elif DEBUG:
                yield from client.send_message(message.channel, '[moobot debug] %s' % str(d_diff))
        else:
            # new channel to the harambe meme
            # just store the current time
            d_new = message.timestamp

            c.execute('insert into harambe values (?, "' + str(d_new) + '")', channel_id)
            conn.commit()

# connect to the DB
conn = sqlite3.connect('respect.db')
c = conn.cursor()


# initialise if necessary
c.execute('''create table if not exists respect
             (user text, f integer) ''')
# user is the discord user id
# f is an integer with the number of times a user has paid respects

c.execute('''create table if not exists harambe
             (channel text, last text)''')
# channel is a discord channel id
# last is a datetime containing the last noted harambe reference



# compile a regex for matching
r = re.compile('[f|F|x|X]')


client.run('token')
