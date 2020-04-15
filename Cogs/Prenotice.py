from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
import asyncio

class Prenotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog('Config').config['PRENOTICE']
        self.reserved = []
    @commands.command()
    async def prenotice(self, ctx, oparater):
        pass
    @tasks.loop(seconds=60)
    async def loop(self):
        prenotices = [
            {"weekday":2,"hour":23,"minute":40,"_id": 1},
        ]
        for prenotice in prenotices:
            now = datetime.now()
            if not now.weekday() == prenotice.get("weekday"):
                continue
            if prenotice.get("_id") in self.reserved: 
                continue
            target_seconds = prenotice.get("hour")*3600+prenotice.get("minute")*60
            current_seconds= now.hour*3600+now.minute*60+now.second
            delta = target_seconds - current_seconds
            if delta > 0 and delta < 310:
                asyncio.ensure_future(self.send_prenotice(prenotice, delta))
                channel = self.bot.get_channel(self.config.getint('channel'))

    async def send_prenotice(self, prenotice, delay:int):
        self.reserved.append(prenotice.get("_id"))
        await asyncio.sleep(delay)
        channel = self.bot.get_channel(self.config.getint('channel'))
        embed = discord.Embed()
        embed.add_field(name="test",value="test value")
        now = datetime.now()
        await channel.send(embed=embed)
        self.reserved.remove(prenotice.get("_id"))
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop.start()

def setup(bot):
    bot.add_cog(Prenotice(bot))
