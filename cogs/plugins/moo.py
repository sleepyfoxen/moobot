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
            elif re.match('^(m)(o{2,})(\W*)$', message.content.lower(), re.I):
                await bot.process_commands(message)


    @commands.command()
    async def reply(self) -> None:
        """Heh nothing personnel kid"""
        match = re.match('^(m)(o{2,})(\W*)$', message.content.lower(), re.I)
        if len(message.content) == 1994:
            message = message.content
        else:
            message = mooScale(mooReply(match.group, lambda x: x*2))
        await bot.send_message(message.channel, message)

    def mooReply(matchGroups: list, stylingFxn: str):
        # (list, str => str) => list
        return list(map(stylingFxn, matchGroups))

    def mooScale(inputList: list):
        """
        Data type: list => str
        Scales the mooing reply if it's longer than the max char limit of 1994
        ------
        Parameter:
            inputList = List of match groups to reduce if needed
        Returns:
            The list of match groups joined to form the reply string
        """
        reducedInputList = inputList
        i = 0
        while len(''.join(reducedInput)) > 1994:
            reducedInputList[i] = removeIfNotOneLetter(inputList[i])
            i = (i + 1) % len(reducedInputList)
        return ''.join(reducedInputList)

    def removeIfNotOneLetter(input: str):
        """
        Data type: str => str
        Removes one letter off the input string if it isn't already only
        one character long.
        ------
        Parameter:
            input = The input string which last letter is to be removed
        Returns:
            The input string with its last letter removed
        """
        return len(input) > 1? input[:-1] : input

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
