# grabs and provides all the commands
# Quick note: here a 'plugin' is a cog


import os
from functools import partial
import logging

from pluginbase import PluginBase


# see https://github.com/mitsuhiko/pluginbase/blob/master/example/example.py
# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

# Setup a plugin base for moobot
plugin_base = PluginBase(package='moobot-plugins')

# Search for plugins (cogs)
source = plugin_base.make_plugin_source(
    searchpath=[get_path('plugins')],
    identifier='moobot')

plugins = []


# Run each cog's set up code
for plugin_name in source.list_plugins():
    plugin = source.load_plugin(plugin_name)
    try:
        plugin.setup()
    except AttributeError as e:
        logging.error('%s could not be loaded: no setup() function',
                      plugin.__name__)

    else:
        plugins.append(plugin)

