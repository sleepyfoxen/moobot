# have you mooed today?

import logging
import re

import discord
from discord.ext import commands


class Moo:
    """Moo"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.author.id == bot.user.id:
                return
            if message.content.lower() == 'moo':
                await bot.process_commands(message)
            elif re.match('^mo{2,}\W*$', message.content.lower()):
                await bot.send_message(message.channel, 'mooooooooooooooooo')


    @commands.command()
    async def reply(self) -> None:
        """Heh nothing personnel kid"""
        # TODO: look out for maximum message size
        match = re.match('^(m)(o{2,})(\W*)$', message.content.lower()):
        message = match.group[1] + 2*match.group[2] + 2*match.group[3];
        await bot.send_message(message.channel, message)

    @commands.command()
    async def moo(self) -> None:
        """moo"""
        message = '''```
         (__)
         (oo)
   /------\/
  / |    ||
 *  /\---/\\
    ~~   ~~
...."Have you mooed today?"...```
        '''
        await self.bot.say(message)


def setup() -> None:
    logging.info('Moo cog is being set up')
    return


def cog() -> Moo:
    logging.info('Moo cog is being registered')
    return Moo
