from discord.ext import commands, tasks
from datetime import datetime

class Prenotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog('Config').config['PRENOTICE']
    @commands.command()
    async def prenotice(self, ctx, oparater):
        pass
    @tasks.loop(seconds=60)
    async def loop(self):
        now = datetime.utcnow()
        channel = self.bot.get_channel(self.config.getint('channel'))
        await channel.send(now.strftime('Its %Y/%m/%d %H:%M:%S'))
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop.start()

def setup(bot):
    bot.add_cog(Prenotice(bot))
