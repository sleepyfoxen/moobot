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

fixed_karma = {
    '1337': 1337
}

log_level = logging.INFO  # everything
log_file = 'moobot.log'