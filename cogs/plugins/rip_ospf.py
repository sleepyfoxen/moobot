#Dark Blue on black is really hard to read, putty. Thhanks 

import logging

import discord
from discord.ext import commands

class Rip_Ospf:
    """Makes users aware of the superior routing algorithm"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.content.lower() in ('rip', 'Rip', 'RIP'):
                await bot.process_commands(message)


    @commands.command(pass_context=True,
                      aliases=['rip', 'Rip', 'RIP'])
    async def rip_ospf(self, ctx: commands.Context) -> None:
        """Makes users aware of the superior routing algorithm"""

        await self.bot.say(':regional_indicator_o: :regional_indicator_s: :regional_indicator_p: :regional_indicator_f:')


def setup() -> None:
    logging.info('ripospf set up.')
    # no setup needed.

def cog() -> Rip_Ospf:
    logging.info('registering ripospf cog.')
    return Rip_Ospf
