from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

class Prenotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog('Config').config['PRENOTICE']
        self.reserved = []
        self.schedules = []
        self.read_json('wb.json')
    def read_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for read_schedule in json_data.get("schedule"):
            advances = json_data.get('advance')
            if 'advance' in read_schedule.keys():
                advances = read_schedule.get('advance')
            for advance in advances:
                schedule = read_schedule.copy()
                schedule["thumbnail"] = json_data.get("boss").get(schedule.get("boss"))
                schedule["advance"] = advance
                if schedule not in self.schedules:
                    self.schedules.append(schedule)
    @commands.command()
    async def prenotice(self, ctx):
        pass
    @tasks.loop(minutes=5)
    async def loop(self):
        for prenotice in self.schedules:
            now = datetime.now()
            if not now.weekday() == prenotice.get("weekday"):
                continue
            if prenotice in self.reserved: 
                logger.debug(f"prenotice: {prenotice} is already reserved")
                continue
            target_seconds = prenotice.get("hour")*3600+prenotice.get("minute")*60 - prenotice.get("advance")
            current_seconds= now.hour*3600+now.minute*60+now.second
            delta = target_seconds - current_seconds
            if delta > 0 and delta < 310:
                logger.debug(f"ensured task: {prenotice}")
                asyncio.ensure_future(self.send_prenotice(prenotice, delta))

    async def send_prenotice(self, prenotice, delay:int):
        self.reserved.append(prenotice)
        logger.debug(f"{prenotice} is append reserved list")
        await asyncio.sleep(delay)
        channel = self.bot.get_channel(self.config.getint('channel'))
        embed = discord.Embed(title=prenotice.get('title'))
        advance = prenotice.get("advance")
        if 'value' not in prenotice:
            value = f"出現 {int(advance/60)} 分前" if advance > 60 else f"出現 {advance} 秒前"
        else:
            value = prenotice.get('value')
        embed.add_field(name=prenotice.get('boss'),value=value)
        embed.set_thumbnail(url=prenotice.get("thumbnail"))
        await channel.send(embed=embed)
        self.reserved.remove(prenotice)
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop.start()

def setup(bot):
    bot.add_cog(Prenotice(bot))
