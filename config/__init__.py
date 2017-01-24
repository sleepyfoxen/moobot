"""moobot settings"""

import logging

# the log in details for the account moobot uses
# please use an API token if you can
# as email address / password based login is depricated
moobot_login = {
    'discord_token': None,
    'email': None,
    'password': None
}

if moobot_login['discord_token'] is None and moobot_login['email'] is None:
    raise RuntimeError('Neither token nor email provided. Please read the '
                       'README.md file.')

# this is the "now playing" game
status_message = 'can moobot dream of electric sheep?'

database_file = 'moobot.db'

fixed_respect = {
    '1337': '1337'
}


# things I should store in a database
subscribed_servers = {
    # server_id

    '242660481792344064': { # moo
        'announce_channel_id': '273235427966713857',
        'default_roles': ('273236044533465088',)
    }
}




log_level = logging.INFO
# log_file = 'moobot.log'  # log to file
log_file = None  # log to console
