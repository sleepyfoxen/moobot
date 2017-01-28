
import datetime
import logging

import discord
from discord.ext import commands

from db import c, conn


class Harambe:
    """may he rest in peace"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        @self.bot.listen('on_message')
        async def match(message: discord.Message) -> None:
            if 'harambe' in message.content.lower():
                await bot.process_commands(message)

    @commands.command(pass_context = True)
    async def harambe(self, ctx: commands.Context) -> None:
        """forever in our ~~memes~~ hearts"""

        if ctx.message.server is None:
            return

        server_id = ctx.message.server.id
        c.execute('select * from harambe where server=?', (server_id,))
        result = c.fetchone()

        # result: [ server_id, last, number, chain, max ]

        if result is not None:
            # previous server
            # message.timestamp is a native datetime.datetime object
            # so in the database we are storing a datetime.datetime object
            # (=> str(datetime.datetime), it's a string-encoded ISO-based date)
            d_last = datetime.datetime.strptime(result[1],
                                                '%Y-%m-%d %H:%M:%S.%f')
            d_new = ctx.message.timestamp
            d_diff = d_new - d_last

            if d_diff.days >= 2:
                # update last in db
                c.execute('''update harambe
                                set last=?, number=number+1, chain=0
                                where server=?''', (str(d_new), server_id))
                conn.commit()
                await self.bot.say('days since harambe was last mentioned: '
                                   '%s --> 0' % d_diff.days)

            elif d_diff.days == 1:
                if result[3] >= result[4]:
                    c.execute('update harambe set max=?', (result[3] + 1,))

                c.execute('''update harambe
                                set last=?, number=number+1, chain=chain+1
                                where server=?''', (str(d_new), server_id))
                conn.commit()
                await self.bot.say('daily harambe chain: %s'
                                   % str(result[3] + 1))

            else:
                c.execute('''update harambe
                                set number=number+1
                                where server=?''', (server_id,))
                conn.commit()

        else:
            d_new = ctx.message.timestamp
            c.execute('''insert into harambe
                            values (?, ?, 1, 0, 0)''', (server_id, str(d_new)))

            conn.commit()


def setup() -> None:
    logging.info('harambe cog is being set up')
    c.execute('''create table if not exists harambe
                (server text, last text,
                 number integer, chain integer, max integer)''')

def cog() -> Harambe:
    logging.info('harambe cog is being registered')
    return Harambe
