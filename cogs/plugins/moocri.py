# have you mooed today?

import logging
import re

import discord
from discord.ext import commands


class Moocri:
    """When you cry, moobot cries with you too"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.author.id == bot.user.id:
                return
            if re.match('^[mM]oocri$', message.content):
                await bot.process_commands(message)


    @commands.command(aliases=['Moocri'])
    async def moocri(self) -> None:
        """A cri"""
        message = ':sweat_drops: :cow: :sweat_drops:'
        await self.bot.say(message)

def setup() -> None:
    logging.info('Moocri cog is being set up')
    return


def cog() -> Moocri:
    logging.info('Moocri cog is being registered')
    return Moocri
