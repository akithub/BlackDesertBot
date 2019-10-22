from discord.ext import commands

import configparser

class Config(commands.Cog):
    def __init__(self, bot, config_path):
        self.bot = bot
        self.read_config(config_path)
    def read_config(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

def setup(bot):
    bot.add_cog(Config(bot, 'config.ini'))
