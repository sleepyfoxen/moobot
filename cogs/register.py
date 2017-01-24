import logging

from discord.ext.commands import Bot


cog_handles = []


# Register each plugin
def register(plugins: list, bot: Bot) -> None:
    """Registers each plugin"""
    for plugin in plugins:

        # two things:
        # 1. register the command as a cog
        # 2. register any ways of triggering the command (eg: 'f')
        try:
            cog = plugin.cog()
            cog_name = cog.__name__
            cog = cog(bot)
            _ = plugin.setup.__name__
            bot.add_cog(cog)
            cog_handles.append(bot.get_cog(cog_name))
        except AttributeError as e:
            logging.error('%s could not be loaded since it is '
                                       'missing an attribute. Please check '
                                       'it has both a cog function returning '
                                       'its cog, and a setup function',
                                        plugin.__name__)