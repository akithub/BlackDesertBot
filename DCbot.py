import discord

import config

TOKEN = config.TOKEN

TARGET_TEXT_CHANNEL_ID  = config.TARGET_TEXT_CHANNEL_ID
TARGET_VOICE_CHANNEL_ID = config.TARGET_VOICE_CHANNEL_ID
GUILD_ID = config.GUILD_ID


client = discord.Client()

@client.event
async def on_voice_state_update(member, before, after): 
    if member.guild.id == GUILD_ID and (before.channel != after.channel):
        alert_channel = client.get_channel(TARGET_TEXT_CHANNEL_ID)
        if after.channel.id == TARGET_VOICE_CHANNEL_ID: 
            msg = f'__**{member.name}**__ が VC 参加'
            await alert_channel.send(msg)
        elif before.channel.id == TARGET_VOICE_CHANNEL_ID: 
            msg = f'__**{member.name}**__ が VC 退出'
            await alert_channel.send(msg)

client.run(TOKEN)