import discord

import config

TOKEN = config.TOKEN

VCINOUT_TARGET_TEXT_CHANNEL_ID  = config.VCINOUT_TARGET_TEXT_CHANNEL_ID
VCINOUT_TARGET_VOICE_CHANNEL_ID = config.VCINOUT_TARGET_VOICE_CHANNEL_ID
GUILD_ID = config.GUILD_ID



class SetsugekkaBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.kujira_mesr_ids=[]
        self.kujira_mes = """
        捜索完了CH：
        Ba {0[Ba1]} {0[Ba2]} {0[Ba3]} {0[Ba4]}
        Se {0[Se1]} {0[Se2]} {0[Se3]} {0[Se4]}
        Me {0[Me1]} {0[Me2]} {0[Me3]} {0[Me4]}
        Va {0[Va1]} {0[Va2]} {0[Va3]} {0[Va4]}
        Mg {0[Mg1]} {0[Mg2]} {0[Mg3]} {0[Mg4]}
        ka {0[Ka1]} {0[Ka2]} {0[Ka3]}
        """
        self.init_kujira_state()
        self.kujira_mesr_ids = []
        self.channel_emoji = {
            1: '1⃣',
            2: '2⃣',
            3: '3⃣',
            4: '4⃣',
        }
    def init_kujira_state(self):
        self.kujira_state = {
            'Ba1': '', 'Ba2': '', 'Ba3':'', 'Ba4': '',
            'Se1': '', 'Se2': '', 'Se3':'', 'Se4': '',
            'Me1': '', 'Me2': '', 'Me3':'', 'Me4': '',
            'Va1': '', 'Va2': '', 'Va3':'', 'Va4': '',
            'Mg1': '', 'Mg2': '', 'Mg3':'', 'Mg4': '',
            'Ka1': '', 'Ka2': '', 'Ka3':'',
        }
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == GUILD_ID and (before.channel != after.channel):
            alert_channel = self.get_channel(TARGET_TEXT_CHANNEL_ID)
            if after.channel and after.channel.id == VCINOUT_TARGET_VOICE_CHANNEL_ID:
                msg = f'__**{member.name}**__ が VC 参加'
                await alert_channel.send(msg)
            elif before.channel and before.channel.id == VCINOUT_TARGET_VOICE_CHANNEL_ID:
                msg = f'__**{member.name}**__ が VC 退出'
                await alert_channel.send(msg)

    async def on_message(self, message):
        # 自分自身に反応しないように
        if self.user != message.author:
            # for comannd: +kujira
            if message.content==('+kujira'):
                self.init_kujira_state()
                self.kujira_checked_mes = await message.channel.send(self.kujira_mes.format(self.kujira_state))
                self.kujira_title_mes = await message.channel.send('=============================\n未捜索CH')
                emj = self.channel_emoji
                msgb = await message.channel.send('Ba')
                await msgb.add_reaction(emj[1])
                await msgb.add_reaction(emj[2])
                await msgb.add_reaction(emj[3])
                await msgb.add_reaction(emj[4])
                msgs = await message.channel.send('Se')
                await msgs.add_reaction(emj[1])
                await msgs.add_reaction(emj[2])
                await msgs.add_reaction(emj[3])
                await msgs.add_reaction(emj[4])
                msgme = await message.channel.send('Me')
                await msgme.add_reaction(emj[1])
                await msgme.add_reaction(emj[2])
                await msgme.add_reaction(emj[3])
                await msgme.add_reaction(emj[4])
                msgv = await message.channel.send('Va')
                await msgv.add_reaction(emj[1])
                await msgv.add_reaction(emj[2])
                await msgv.add_reaction(emj[3])
                await msgv.add_reaction(emj[4])
                msgmg = await message.channel.send('Mg')
                await msgmg.add_reaction(emj[1])
                await msgmg.add_reaction(emj[2])
                await msgmg.add_reaction(emj[3])
                await msgmg.add_reaction(emj[4])
                msgk = await message.channel.send('Ka')
                await msgk.add_reaction(emj[1])
                await msgk.add_reaction(emj[2])
                await msgk.add_reaction(emj[3])
                self.kujira_mesr_ids = {msgb.id:'Ba', msgs.id:'Se', msgme.id:'Me', msgv.id:'Va', msgmg.id:'Mg', msgk.id:'Ka'}

    async def on_reaction_add(self, reaction, user):
        # for command: +kujira
        if self.kujira_mesr_ids:
            if reaction.message.id in self.kujira_mesr_ids.keys() and user != self.user:
                await reaction.message.remove_reaction(reaction, self.user)
                await reaction.message.remove_reaction(reaction, user)
                inv_emoji = {v:k for k, v in self.channel_emoji.items()}
                BOChannel = self.kujira_mesr_ids[reaction.message.id]+str(inv_emoji[str(reaction)])
                self.kujira_state[BOChannel] = str(reaction)
                await self.kujira_checked_mes.edit(content=self.kujira_mes.format(self.kujira_state))
                if not reaction.message.reactions:
                    await reaction.message.delete()

client = SetsugekkaBot()
client.run(TOKEN)