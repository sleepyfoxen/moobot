"""moobot
moobot is a shitty discord bot that helps people
pay their respects
"""

import logging
import config

# set up logging
if config.log_file is None:
    logging.basicConfig(level=config.log_level)
else:
    logging.basicConfig(filename=config.log_file, level=config.log_level)

import discord
from discord.ext import commands

import cogs


# set up bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or(''),
            description='a shitty discord bot for respect and other bad memes')

# set up commands
cogs.register(cogs.plugins, bot)
logging.warning('attempting to load %s cogs', str(len(bot.cogs)))


@bot.event
async def on_ready() -> None:
    logging.info('%s - %s', bot.user.name, bot.user.id)
    logging.info('playing: %s', config.status_message)
    await bot.change_presence(
        game=discord.Game(name='%s' % config.status_message))


@bot.event
async def on_message(message: discord.Message) -> None:

    # Don't trigger on our own messages
    if message.author.id == bot.user.id:
        return

    if message.content.startswith(bot.user.mention):  # someone tagged moobot
        message.content = message.content.split(bot.user.mention + ' ')[1]+ ' '
        # catch the space after the @moobot, and add a space at the end
        # saying that this isn't a hack would be a bit misrepresentative
        await bot.process_commands(message)


if config.moobot_login['discord_token'] is not None:
    bot.run(config.moobot_login['discord_token'])

else:
    bot.run(config.moobot_login['email'],
        config.moobot_login['password'])
