from discord.ext import commands

import discord
import logging

logger = logging.getLogger(__name__)

class VCinout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog('Config').config['VOICE_INOUT']
        self.guild_id = self.config.getint("guild_id")
        self.output_channel_id = self.config.getint("output_channel_id")
        self.voice_channel_id = self.config.getint("voice_channel_id")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == self.guild_id and (before.channel != after.channel):
            alert_channel = self.bot.get_channel(self.output_channel_id)
            if after.channel and after.channel.id == self.voice_channel_id:
                msg = f'__**{member.name}**__ が VC 参加'
                await alert_channel.send(msg)
            elif before.channel and before.channel.id == self.voice_channel_id:
                msg = f'__**{member.name}**__ が VC 退出'
                await alert_channel.send(msg)

def setup(bot):
    bot.add_cog(VCinout(bot))