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
            elif re.match('^(m+)(o{2,})(\W*)$', message.content.lower(), re.I):
                await self.reply(message)


    async def reply(self, message: discord.Message) -> None:
        """Heh nothing personnel kid"""
        channel = message.channel

        match = re.match('^(m+)(o{2,})(\W*)$', message.content.lower(), re.I)
        if len(message.content) == 1994:
            message = message.content
        else:
            message = self.moo_scale(self.moo_reply(match.groups(),
                                                    lambda x: x * 2))
        await self.bot.send_message(channel, message)

    @staticmethod
    def moo_reply(match_groups: tuple, styling_fxn) -> list:
        # (list, str => str) -> list
        return list(map(styling_fxn, match_groups))

    def moo_scale(self, input_list: list) -> str:
        """
        Data type: list -> str
        Scales the mooing reply if it's longer than the max char limit of 1994
        ------
        Parameter:
            inputList = List of match groups to reduce if needed
        Returns:
            The list of match groups joined to form the reply string
        """
        reduced_input_list = input_list
        i = 0
        while len(''.join(reduced_input_list)) > 1994:
            reduced_input_list[i] = self.remove_if_not_one_letter(input_list[i])
            i = (i + 1) % len(reduced_input_list)
        return ''.join(reduced_input_list)

    @staticmethod
    def remove_if_not_one_letter(input: str) -> str:
        """
        Data type: str -> str
        Removes one letter off the input string if it isn't already only
        one character long.
        ------
        Parameter:
            input = The input string which last letter is to be removed
        Returns:
            The input string with its last letter removed
        """

        if len(input) > 1:
            return input[:-1]
        else:
            return input

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
