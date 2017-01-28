# have you mooed today?

import logging

import discord
from discord.ext import commands


class Moo:
    """Moo"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.content.lower() == 'moo':
                await bot.process_commands(message)


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

