
import logging
import subprocess

from random import choice

import discord
from discord.ext import commands


class Fortune:
    """runs fortune | cowsay and says the result"""

    def __init__(self, bot):
        self.bot = bot
        self.cows = None

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if message.content.lower() in {'fortune | cowsay', 'fortune'}:
                await bot.process_commands(message)



    def get_cows(self) -> list:
        if getattr(self, 'cows', None) is not None:
            return self.cows

        cowsay_string = subprocess.check_output(['cowsay', '-l'])

        try:
            cowsay_string = cowsay_string.decode('utf-8')
        except Exception as e:
            logging.error('get_cows err %s' % e)
            return
        cowsay_lines = cowsay_string.split('\n')

        # the first line is not helpful
        cowsay_lines = cowsay_lines[1:]

        cowsays = []
        for line in cowsay_lines:
            cows = line.split(' ')
            cowsays += cows

        self.cows = cowsays
        return cowsays


    @commands.command(aliases=['fortune | cowsay'])
    async def fortune(self):
        """fortune"""
        cow = ''
        while cow == '':
            cow = choice(self.get_cows())

        fortune = subprocess.check_output(['fortune'])
        cowsay = subprocess.check_output(['cowsay', '-f', cow, fortune])

        try:
            cowsay = cowsay.decode('utf-8')
        except Exception as e:
            logging.error('%s' % e)
            return

        cowsay = '```' + cowsay + '```'

        await self.bot.say(cowsay)


def setup() -> None:
    logging.info('fortune cog is being set up')


def cog() -> Fortune:
    logging.info('fortune cog is being registered')
    return Fortune