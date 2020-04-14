from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
import asyncio

class Prenotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog('Config').config['PRENOTICE']
    @commands.command()
    async def prenotice(self, ctx, oparater):
        pass
    @tasks.loop(seconds=60)
    async def loop(self):
        db = [{"weekday":1,"hour":23,"minute":00}]
        now = datetime.now()
        await channel.send(now.strftime('Its %Y/%m/%d %H:%M:%S'))
        asyncio.ensure_future(self.send_prenotice(10))
    async def send_prenotice(self, delay:int):
        await asyncio.sleep(delay)
        channel = self.bot.get_channel(self.config.getint('channel'))
        embed = discord.Embed()
        embed.add_field(name="test",value="test value")
        now = datetime.now()
        await channel.send(now.strftime('Its %Y/%m/%d %H:%M:%S'))
        await channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop.start()

def setup(bot):
    bot.add_cog(Prenotice(bot))
