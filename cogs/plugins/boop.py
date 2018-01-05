import logging

import discord
from discord.ext import commands


class Boop:
    """boops you x3"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.author.id == bot.user.id:
                return
            if message.content.lower() in {'boop', '!do a boop'}:
                await self.boop(message)


    async def boop(self, message: discord.Message) -> None:
        await self.bot.send_message(message.channel,
                                    '*%s boops %s x3*' %
                                    (self.bot.user.mention, message.author.mention))

def setup() -> None:
    logging.info('boop cog is being set up')
    return

def cog() -> Boop:
    logging.info('boop cog is being registered')
    return Boop