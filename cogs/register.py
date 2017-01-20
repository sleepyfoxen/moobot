import logging

from discord.ext.commands import Bot


cog_handles = []


# Register each plugin
def register(plugins: list, bot: Bot):
    """Registers each plugin"""
    for plugin in plugins:

        # two things:
        # 1. register the command as a cog
        # 2. register any ways of triggering the command (eg: 'f')
        try:
            cog = plugin.cog()(bot)

            bot.add_cog(cog)
            cog_handles.append(bot.get_cog(plugin.cog().__name__))
        except AttributeError as e:
            logging.log(logging.ERROR, '%s could not be loaded since it is '
                                       'missing an attribute. Please check '
                                       'it has both a cog function returning '
                                       'its cog,' % plugin.__name__)