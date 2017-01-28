# new_member.py does two things:
# firstly, it announces to the server on a registered channel that there's
# a new member.

# secondly, it tries to assign them a 'default' role.

# this code was originally written by superwool, and adapted to fit in cog
# loading system.

import logging

import discord
from discord.ext import commands

from config import subscribed_servers


class AnnounceNewBrother:

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_member_join')
        async def welcome(member: discord.Member) -> None:
            await self.welcome(member)


    async def welcome(self, member: discord.Member) -> None:
        logging.debug('new member: %s %s', member.server.name,
                      member.display_name)

        logging.debug('bot is at: %s', self.bot)

        # check that this server is subscribed to default channel setting
        # (or announce)
        if not member.server.id in subscribed_servers:
            logging.debug('skipping... ')
            return

        server = subscribed_servers[member.server.id]
        channel = member.server.get_channel(server['announce_channel_id'])

        # welcome the new member by sending a message to the subscribed
        # channel
        await self.bot.send_message(channel, 'ohai! Welcome to the server, %s!'
                         % member.mention)

        logging.debug('tried to send the message to %s', channel.name)

        # now try to set some roles
        server_roles = member.server.roles
        logging.debug('roles: %s', server_roles)
        default_roles = [role for role in server_roles
                         if (role.id in server['default_roles'])]

        logging.debug('default_roles: %s', default_roles)

        # don't try to change roles if there are none configured
        if len(default_roles) == 0:
            return

        try:
            await self.bot.replace_roles(member, *default_roles)
        except discord.Forbidden as e:
            # We don't have permission to do this
            logging.warning("Couldn't set roles: %s", e)


def setup() -> None:
    logging.info('AnnounceNewBrother cog is being set up')
    # TODO: move hard coded server registrations into sqlite3
    # and set up the table here
    return


def cog() -> AnnounceNewBrother:
    logging.info('AnnounceNewBrother cog is being registered')
    return AnnounceNewBrother