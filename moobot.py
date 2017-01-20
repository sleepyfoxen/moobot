"""moobot
moobot is a shitty discord bot that helps people
pay their respects
"""

import logging
import sqlite3
import re

import discord
from discord.ext import commands

import config
import commands as command

logging.basicConfig(level=logging.INFO)



class Respect:
    """Press f to pay respects."""

    def __init__(self, bot):
        self.bot = bot
        self.conn = conn
        self.c = c

    @commands.command(pass_context=True,
        aliases=['F', 'x', 'X', 'Blep', 'blep'])
    async def f(self, ctx):
        """pays respects"""
        await command.f(self, ctx)

    @commands.command(pass_context=True,
        aliases=['Respect', 'r', 'actualrespect', 'realrespect'])
    async def respect(self, ctx):
        """displays how much respect the user has"""
        await command.respect(self, ctx)

    @commands.command(pass_context=True)
    async def top(self, ctx):
        """displays the people with the most respect"""
        await command.top_respect(self, ctx)

class Harambe:
    """Harambe related commands.

    Harambe on moobot works as follows:
    1. work out how long since harambe was last mentioned
    2. * if it's more than one day, display the difference in days+
       * if it's exactly one day, display and update the chain variable+
       * if it's less than one day, do nothing
    3. except in the third case, reset the last mentioned data
    4. update the counter
    """

    def __init__(self, bot):
        self.bot = bot
        self.conn = conn
        self.c = c

    @commands.command(pass_context=True)
    async def harambe(self, ctx):
        """resets the harambe counter"""
        await command.harambe(self, ctx)


class WithRice:
    """A retired meme"""

    def __init__(self, bot):
        self.bot = bot
        self.conn = conn
        self.c = c

    @commands.command(pass_context=True)
    async def with_rice(self, ctx):
        """spicy memes return to moobot? nah"""
        await commands.with_rice

class OneTwoTwoTwoThreeFourFive:
    """just don't ask"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def one_two_two_two_three_four_five(self, ctx):
        """just don't ask"""
        await command.one_two_two_two_three_four_five(self, ctx)

class CopyPasta:
    """don't know why I made this"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def copy_pasta(self, ctx):
        """memify your text"""

class Moo:
    """Moo"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def moo(self, ctx):
        await command.moo(self, ctx)

# connect to the DB
conn = sqlite3.connect(config.database_file)
c = conn.cursor()


# initialise if necessary
c.execute('''create table if not exists respect
             (user text, f integer) ''')
# user is the discord user id
# f is an integer with the number of times a user has paid respects

c.execute('''create table if not exists harambe
             (server text, last text,
              number integer, chain integer, max integer)''')
# channel is a discord channel id
# last is a datetime containing the last noted harambe reference

c.execute('''create table if not exists ratings
              (thing text, rater text,
              without integer, with integer)''')



bot = commands.Bot(command_prefix=commands.when_mentioned,
    description='a shitty discord bot for respect and harambe')
bot.add_cog(Harambe(bot))
bot.add_cog(Respect(bot))
bot.add_cog(OneTwoTwoTwoThreeFourFive(bot))
bot.add_cog(WithRice(bot))
bot.add_cog(Moo(bot))

harambe = bot.get_cog('Harambe')
respect = bot.get_cog('Respect')
one_two = bot.get_cog('OneTwoTwoTwoThreeFourFive')
with_rice = bot.get_cog('WithRice')
moo_cog = bot.get_cog('Moo')
announce_new_brother = bot.get_cog('AnnounceNewBrother')

password_matcher = re.compile('122+345') # 1222*345
with_rice_matcher = re.compile('.*[0-9]+/10.*')
role_change_matcher = re.compile('^!change_role of (\d+?) to (\w+?)')


# TODO: Map the cog strings to a single variable
logging.log(msg='cogs: %s %s %s %s %s %s' % (harambe, respect, one_two, with_rice, moo_cog, announce_new_brother),
            level=logging.INFO)

# helper function
def context_factory(message, bot):
    return commands.Context(message = message,
                            bot = bot,
                            args = [],
                            kwargs = {},
                            prefix = '',
                            command = message.content)

@bot.event
async def on_ready():
    logging.log(msg='%s - %s' % (bot.user.name, bot.user.id),
        level=logging.INFO)
    logging.log(msg='playing: %s' % config.status_message,
        level=logging.INFO)
    await bot.change_presence(
        game=discord.Game(name='%s' % config.status_message))

@bot.event
async def on_message(message):
    # print(message.content.lower())
    # don't trigger on own messages
    if message.author.id == bot.user.id:
        pass

    elif message.content.lower() in ['f', 'x', 'blep']:
        await command.f(respect, context_factory(message, respect))
    elif message.content.lower() in ['respect', 'actualrespect', 'realrespect']:
        await command.respect(respect, context_factory(message, respect))
    elif message.content.lower() == 'top':
        await command.top_respect(respect, context_factory(message, respect))
    elif 'harambe' in message.content.lower():
        await command.harambe(harambe, context_factory(message, harambe))
    elif with_rice_matcher.match(message.content):
        await command.with_rice(WithRice, context_factory(message, with_rice))
    elif password_matcher.match(message.content):
        await command.one_two_two_two_three_four_five(one_two,
                                            context_factory(message, one_two))
    elif message.content.lower() in ['apt-get moo', 'moo']:
        await command.moo(moo_cog, context_factory(message, moo_cog))
    elif role_change_matcher.match(message.content.lower()):
        try:
            print("Matched")
            result = role_change_matcher.match(message.content.lower())
            member = server.getMember(id=result[0])
            role = [discord.Role(name=result[1])]
            await bot.replace_roles(member, *role)
            await bot.send_message(message.channel, "{}'s role changed to {}".format(member.name, role.name))
        except discord.Forbidden:
            print("Don't have the permission to do it; message Sara")
        except discord.HTTPException as e:
            print("Got an HTTPException: {} {} ".format(e.response.status, e.response.reason))

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await command.announce_new_brother(announce_new_brother,
            context_factory(member, announce_new_brother))

if config.moobot_login['discord_token'] is not None:
    bot.run(config.moobot_login['discord_token'])
else:
    bot.run(config.moobot_login['email'],
        config.moobot_login['password'])
