"""holds moobots commands"""
import asyncio
import datetime

import config
import discord

import compose as _

async def harambe(cls_, ctx):
    """harambe counter"""
    # need to reset the number of days since harambe was last mentioned
    # 1. check if the server has ever crumbed before
    # -> either reset date to current time or start a counter
    if ctx.message.server is None:
        return # probably a PM

    server_id = (ctx.message.server.id,)

    cls_.c.execute('select * from harambe where server=?',
                    server_id)
    result = cls_.c.fetchone()

    # result = [server, last, number, chain, max]

    if result is not None:
        # previous server
        # message.timestamp is a native datetime.datetime object
        # so in the database we are storing a datetime.datetime object
        # (=> str(datetime.datetime), it's a string-encoded ISO-based date)
        d_last = datetime.datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S.%f')
        d_new = ctx.message.timestamp
        d = (str(d_new),)

        d_diff = d_new - d_last
        if d_diff.days >= 2:
            # update last in db
            cls_.c.execute('''update harambe
                                set last=?, number=number+1, chain=0
                                where server=?''', [d[0], server_id[0]])
            cls_.conn.commit()
            await cls_.bot.send_message(ctx.message.channel,
                    'days since harambe was last mentioned: %s --> 0'
                                                            % d_diff.days)

        elif d_diff.days == 1:
            if result[3] >= result[4]:
                cls_.c.execute('update harambe set max=?', (result[3] + 1,))

            cls_.c.execute('''update harambe
                                set last=?, number=number+1, chain=chain+1
                                where server=?''', [d[0], server_id[0]])
            cls_.conn.commit()

            await cls_.bot.send_message(ctx.message.channel,
                'daily harambe chain: %s' % str(result[3] + 1))
        else:
            cls_.c.execute('''update harambe
                                set number=number+1
                                where server=?''', server_id)

        if config.DEBUG:
            await cls_.bot.send_message(ctx.message.channel,
                                        '[moobot debug]: %s %s %s'
                                        % (str(d_diff), result[2], result[3]))
    else:
        # new server to the harambe meme
        # just store the current time
        d_new = ctx.message.timestamp
        d = (str(d_new),)

        cls_.c.execute('insert into harambe values (?, ?, 1, 0, 0)',
                        [server_id[0], d[0]])
        cls_.conn.commit()




async def f(cls_, ctx):
    """respect"""

    # we do two things:
    # 1. we increment their respect tallies in sqlite
    # 2. we let everyone know how respectful they are
    u = (ctx.message.author.id,)

    cls_.c.execute('select * from respect where user=?', u)
    u_ = cls_.c.fetchone()
    if u_ is not None:

        cls_.c.execute('update respect set f=f+1 where user=?', u)
        cls_.conn.commit()

    else:
        # add user to db
        cls_.c.execute('insert into respect values(?, 1)', u)
        cls_.conn.commit()

    await cls_.bot.send_message(ctx.message.channel,
                       '%s pays their respects' % ctx.message.author.mention)


async def respect(cls_, ctx):
    """respect count"""
    real = ctx.message.content.lower() in ['actualrespect', 'realrespect']
    r = 0

    if not real and ctx.message.author.id in config.fixed_karma:
        # we have the leet effect
        r = str(config.fixed_karma[ctx.message.author.id])

    else:
        # we're asked for how much respect someone has
        u = (ctx.message.author.id,)
        cls_.c.execute('select * from respect where user=?', u)

        result = cls_.c.fetchone()
        if result is not None:
            r = str(result[1])

    await cls_.bot.send_message(ctx.message.channel,
                        '*%s*: %s respect' % (ctx.message.author.mention, r))


async def top_respect(cls_, ctx):
    """moobot will output the global respect leaders"""

    my_members = {}

    for row in cls_.c.execute('select * from respect'):
        # row -> ( 'user id', amount )
        memer = ctx.message.server.get_member(row[0])
        if memer is not None:
            # keep
            my_members[row[0]] = { 'score' : row[1],
                                   'name': memer.display_name }


    # listify members
    members_stripped = list(my_members.values())

    # limit results
    members_stripped.sort(key=lambda member: member['score'], reverse=True)
    members_stripped = members_stripped[:50]

    message = 'the respect scores are as follows:\n```'
    for member in members_stripped:
        message += '{} - {} respect\n'.format(member['name'], member['score'])

    message += '```'

    # print(message)
    await cls_.bot.send_message(ctx.message.channel,
                                message)


async def emojii_pasta(cls_, ctx):
    """translates text to emoji, see emojityper.com"""
    pass

async def with_rice(cls_, ctx):
    """the spicy with rice meme,
    gone from plaguing reddit to plaguing discord"""
    are_we_riced = 'rice' in ctx.message.content.lower()
    await cls_.bot.send_message("With RICE :rice: :rice: :rice:")

# TODO: this

async def one_two_two_two_three_four_five(cls_, ctx):
    """don't ask"""

    await cls_.bot.send_message(ctx.message.channel, ctx.message.content)

async def aptgetmoo(cls_, ctx):
    """moo"""
    message = '''```
             (__)
             (oo)
       /------\/
      / |    ||
     *  /\---/\\
        ~~   ~~
    ...."Have you mooed today?"...
    ```
    '''
    await cls_.bot.send_message(ctx.message.channel, message)

async def announce_new_brother(cls_, member):
    """A new member of The Cult has joined us, and for this we must give our welcome"""
    gamesoc_server = member.server
    server_roles = gamesoc_server.roles
    roles = ['Greig', 'Not Greig | Members']
    mod_message = "@here we got a new one, and moobot can't assign em the\
    appropriate role for some reason. Someone go do it please thanks"
    alert_mods = _.curry(cls_.bot.send_message,
                gamesoc_server.get_channel('210019390849155072'))
    # TODO: Get the ID for roles
    # Figure out if it's Greig first
    role = _.if_else(is_greig(member), _.curry(get_role, gamesoc_server), roles)
    if len(role) == 1:
        # Alert the mods to change it manually
        await alert_mods(mod_message)
    else:
        try:
            print("Changing them roles yo")
            await cls_.bot.replace_roles(member, *role)
        except discord.Forbidden:
            print("Bot has been forbidden from setting the new guy's\
                    role. Go check it out.")
            await alert_mods(mod_message)
        except discord.HTTPException as e:
            print("Got an HTTPException: {} {}".format(e.response.status,
            e.response.reason))
            await alert_mods(mod_message)
    general_chat = gamesoc_server.get_channel('163647742629904384')
    welcome_message = "Welcome to the server {}!".format(member.mention)
    await cls_.bot.send_message(general_chat, welcome_message)

def is_greig(member):
    """Checks if it's Greig. Lmao"""
    return member.id == '105358952753041408'

def get_role(server, wanted_role_name):
    """
    Gets the wanted role (if found) along with the default role
    ------
    Parameters:
        server: The Server object to get the roles from
        wanted_role_name: The name of the desired role
    Returns:
        role: An array with [<wanted role>, <default role>] if the desired role is found,
                or simply [<default role>] if it isn't.
    """
    # TODO: switch to using role ID instead
    role = [next(r for r in server.roles if check_role(r, wanted_role_name), None),
            server.default_role]
    if role[0] is not None:
        print("{} role found. Returning wanted role with default".format(wanted_role_name))
        return role
    print("Role not found. Returning default role {}".format(server.default_role))
    return role[1:]

def check_role(role, wanted_role_name):
    return role.name == wanted_role_name
