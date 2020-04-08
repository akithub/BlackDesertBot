from discord.ext import commands

from configparser import ConfigParser
import os

import logging
import logging.handlers
from logging import getLogger, Filter, DEBUG, INFO

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._config = None
    @property
    def config(self):
        return self._config
    @config.setter
    def config(self, config:ConfigParser):
        self._config = config

def setup(bot):
    bot.add_cog(Config(bot))
