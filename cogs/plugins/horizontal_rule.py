# Inserts horizontal line (eg. to break into a new conversation)

import logging

import discord
from discord.ext import commands

class Horizontal_Line:
    """<hr> or /hr inserts horizontal line"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.content.lower() in ('<hr>', '/hr'):
                await bot.process_commands(message)


    @commands.command(pass_context=True,
                      aliases=['<hr>', '/hr'])
    async def f(self, ctx: commands.Context) -> None:
        """inserts horizontal line (of minus emojis)"""

        await self.bot.say(':heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign::heavy_minus_sign:')


def setup() -> None:
    # no setup needed.

def cog() -> Horizontal_Line:
    logging.info('registering hr cog')
    return Horizontal_Line
