from discord.ext import commands
import discord

import ConfigCog
from Cogs import *

class SetsugekkaBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.load_extension('ConfigCog')
        self.config = self.get_cog('Config').config
        self.load_extension('Cogs.Kujira')
        self.load_extension('Cogs.VCinout')

    async def on_ready(self):
        # print('Logged on as {{0}} (ID: {{0.id}})'.format(self.user))
        print('bot ready')

if __name__ == '__main__':
    client = SetsugekkaBot(command_prefix='+')
    token =  client.config.get('General', 'token')
    client.run(token)