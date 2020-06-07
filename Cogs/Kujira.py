from discord.ext import commands

import discord

class Kujira(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_state()
        self.reacted_mes_ids=[]
        self.mes = """
        捜索完了CH：
        Ba {0[Ba1]} {0[Ba2]} {0[Ba3]} {0[Ba4]}
        Se {0[Se1]} {0[Se2]} {0[Se3]} {0[Se4]}
        Me {0[Me1]} {0[Me2]} {0[Me3]} {0[Me4]}
        Va {0[Va1]} {0[Va2]} {0[Va3]} {0[Va4]}
        Mg {0[Mg1]} {0[Mg2]} {0[Mg3]} {0[Mg4]}
        ka {0[Ka1]} {0[Ka2]} {0[Ka3]}
        """
        self.reacted_mes_ids = []
        self.channel_emoji = {
            1: '1⃣',
            2: '2⃣',
            3: '3⃣',
            4: '4⃣',
        }
    def init_state(self):
        self.state = {
            'Ba1': '', 'Ba2': '', 'Ba3':'', 'Ba4': '',
            'Se1': '', 'Se2': '', 'Se3':'', 'Se4': '',
            'Me1': '', 'Me2': '', 'Me3':'', 'Me4': '',
            'Va1': '', 'Va2': '', 'Va3':'', 'Va4': '',
            'Mg1': '', 'Mg2': '', 'Mg3':'', 'Mg4': '',
            'Ka1': '', 'Ka2': '', 'Ka3':'',
        }
    #  @commands.command(name='kujira')
    async def _generate_reacted_message_id(self, target_CH:str, CH_number:int, ctx:commands.Context):
        mes = await ctx.send(target_CH)
        for i in range(1, CH_number+1):
            await mes.add_reaction(self.channel_emoji[i])
        return mes.id

    @commands.command()
    async def kujira(self, ctx):
        print('kujira command')
        self.init_state()
        self.checked_mes = await ctx.message.channel.send(self.mes.format(self.state))
        self.title_mes = await ctx.message.channel.send('=============================\n未捜索CH')
        target_CH = {'Ba':4, 'Se':4, 'Me':4, 'Va':4, 'Mg':4, 'Ka':3}
        # self.reacted_mes_ids = {msgb.id:'Ba', msgs.id:'Se', msgme.id:'Me', msgv.id:'Va', msgmg.id:'Mg', msgk.id:'Ka'}
        self.reacted_mes_ids = {await self._generate_reacted_message_id(ch, number, ctx):ch for ch, number in target_CH.items()}
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # for command: +kujira
        if self.reacted_mes_ids:
            if reaction.message.id in self.reacted_mes_ids.keys() and user != self.bot.user:
                await reaction.message.remove_reaction(reaction, self.bot.user)
                await reaction.message.remove_reaction(reaction, user)
                inv_emoji = {v:k for k, v in self.channel_emoji.items()}
                # BDのチャンネルと番号を生成 (ex: 'Ba1')
                Ch = self.reacted_mes_ids[reaction.message.id]+str(inv_emoji[str(reaction)])
                self.state[Ch] = str(reaction)
                await self.checked_mes.edit(content=self.mes.format(self.state))
                if not reaction.message.reactions:
                    await reaction.message.delete()
    
def setup(bot):
    bot.add_cog(Kujira(bot))