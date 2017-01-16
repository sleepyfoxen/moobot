"""holds moobots commands"""
import asyncio
import datetime

import config



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
    """translates text to emojii, see emojiityper.com"""
    pass

async def with_rice(cls_, ctx):
    """the spicy with rice meme,
    gone from plaguing reddit to plaguing discord"""
    are_we_riced = 'rice' in ctx.message.content.lower()

# TODO: this

async def one_two_two_two_three_four_five(cls_, ctx):
    """don't ask"""

    await cls_.bot.send_message(ctx.message.channel, ctx.message.content)

async def moo(cls_, ctx):
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
    # TODO: Get the ID for the Not Greig role
    role_name = 'Not Greig | Members'
    role = [next(role for role in server_roles if check_role(role, role_name)),
            gamesoc_server.default_role]
    if role[0].name == role_name:
        print("Changing to Not Greig role")
        try:
            await cls_.bot.replace_roles(member, *role)
        except discord.Forbidden:
            print("Permission ain't set. Go set the permissions")
        except discord.HTTPException as e:
            print("Got an HTTPException: {} {} ".format(e.response.status,
                    e.response.reason))
    else:
        mod_chat_id = '210019390849155072'
        mod_chat = gamesoc_server.get_channel(mod_chat_id)
        # TODO: get the ID for the committee members role
        alert = "@Committee members we got a new one, and moobot can't assign\
                em the appropriate role. Someone go do it please thanks"
        await cls_.bot.send_message(mod_chat, alert)
    general_chat_id = '163647742629904384'
    general_chat = gamesoc_server.get_channel(general_chat_id)
    welcome_message = "Welcome to the server {}!".format(member.mention)
    await cls_.bot.send_message(general_chat, welcome_message)

def check_role(role, res):
    return role.name == res
