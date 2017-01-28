# respect.py
# the original

# press 'f' to pay respects, as well as some handy-dandy tracking
# and stuff

import logging

import discord
from discord.ext import commands

from config import fixed_respect
from db import c, conn



class Respect:
    """press f to pay respects"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.content.lower() in ('f', 'x', 'blep'):
                await bot.process_commands(message)
            elif message.content.lower() in ('respect', 'r', 'actualrespect',
                                             'realrespect'):
                await bot.process_commands(message)
            elif message.content.lower() == 'top':
                await bot.process_commands(message)


    @commands.command(pass_context=True,
                      aliases=['F', 'x', 'X', 'Blep', 'blep'])
    async def f(self, ctx: commands.Context) -> None:
        """pays respects"""
        u = (ctx.message.author.id,)
        c.execute('select * from respect where user=?', u)
        u_ = c.fetchone()

        if u_ is not None:  # user exists in db; increase respect
            c.execute('update respect set f=f+1 where user=?', u)
            conn.commit()

        else:  # user does not exist in db
            c.execute('insert into respect values(?, 1)', u)
            conn.commit()

        await self.bot.say('%s pays their respects'
                           % ctx.message.author.mention)


    @commands.command(pass_context=True,
                      aliases=['Respect', 'r', 'actualrespect', 'realrespect'])
    async def respect(self, ctx: commands.Context) -> None:
        """find out how respectful you are"""
        real = ctx.message.content.lower() in ('actualrespect', 'realrespect')
        r = 0

        if not real and ctx.message.author.id in fixed_respect:
            # we have the leet effect
            r = str(fixed_respect[ctx.message.author.id])

        else:
            # db lookup
            u = (ctx.message.author.id,)
            c.execute('select * from respect where user=?', u)

            result = c.fetchone()
            if result is not None:
                r = str(result[1])

        await self.bot.say('%s: %s respect' % (ctx.message.author.mention, r))


    @commands.command(pass_context=True)
    async def top(self, ctx: commands.Context) -> None:
        """displays who spends too much time on discord"""

        my_members = {}

        for row in c.execute('select * from respect'):
            # row -> ('user_id', amount)
            memer: discord.Member
            memer = ctx.message.server.get_member(row[0])
            # see if this member is on *this* server
            if memer is not None:
                # pop this member into the dictionary
                my_members[row[0]] = { 'score': row[1],
                                       'name': memer.display_name }

        # dictionary -> list of members
        members_stripped = list(my_members.values())

        # sort members
        members_stripped.sort(key=lambda member: member['score'], reverse=True)

        # limit output to fifty members
        members_stripped = members_stripped[:50]

        # build the message
        message = 'these people spend too much time on discord:\n```'
        for member in members_stripped:
            message += '%s - %s respect\n' % (member['name'], member['score'])

        message += '```'

        # send back to the channel
        await self.bot.say(message)


def setup() -> None:
    logging.info('respect cog is being set up')
    c.execute('''create table if not exists respect
                 (user text, f integer)''')
    # user is the discord user id
    # f is an integer with the number of times a user has paid respects


def cog() -> Respect:
    logging.info('registering respect cog')
    return Respect
