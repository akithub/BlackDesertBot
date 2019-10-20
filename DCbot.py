from discord.ext import commands
import discord

import config

from Cogs import *

TOKEN = config.TOKEN

VCINOUT_TARGET_TEXT_CHANNEL_ID  = config.VCINOUT_TARGET_TEXT_CHANNEL_ID
VCINOUT_TARGET_VOICE_CHANNEL_ID = config.VCINOUT_TARGET_VOICE_CHANNEL_ID
GUILD_ID = config.GUILD_ID


class SetsugekkaBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.load_extension('Cogs.Kujira')
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == GUILD_ID and (before.channel != after.channel):
            alert_channel = self.get_channel(TARGET_TEXT_CHANNEL_ID)
            if after.channel and after.channel.id == VCINOUT_TARGET_VOICE_CHANNEL_ID:
                msg = f'__**{member.name}**__ が VC 参加'
                await alert_channel.send(msg)
            elif before.channel and before.channel.id == VCINOUT_TARGET_VOICE_CHANNEL_ID:
                msg = f'__**{member.name}**__ が VC 退出'
                await alert_channel.send(msg)

    async def on_ready(self):
        print('bot ready')

if __name__ == '__main__':
    client = SetsugekkaBot(command_prefix='+')
    client.run(TOKEN)