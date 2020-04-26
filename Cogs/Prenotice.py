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
    @classmethod
    def next_prenotice_datetime(cls, now:datetime, prenotice):
        prenotice_time = datetime(now.year,
                            now.month,
                            now.day + prenotice.get('weekday') - now.weekday(),
                            prenotice.get('hour'),
                            prenotice.get('minute'),
                            0)
        if prenotice_time - now < timedelta(0):
            prenotice_time += timedelta(days=7)
        return prenotice_time

    @commands.command()
    async def prenotice(self, ctx):
        pass
    @tasks.loop(minutes=5)
    async def loop(self):
        for prenotice in self.schedules:
            now = datetime.now()
            if prenotice in self.reserved: 
                logger.debug(f"prenotice: {prenotice} is already reserved")
                continue
            prenotice_time = self.next_prenotice_datetime(now, prenotice)
            delta = prenotice_time - now
            if delta < timedelta(seconds=310):
                logger.debug(f'delta time:{delta}')
                logger.debug(f"ensured task: {prenotice}")
                asyncio.ensure_future(self.send_boss_prenotice(prenotice, delta.total_seconds() - prenotice.get('advance')))

    async def send_boss_prenotice(self, prenotice, delay:int):
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
        msg = await channel.send(embed=embed, delete_after=300)
        if advance <= 10:
            for c in range(1,advance+1):
                await asyncio.sleep(0.8)
                embed.remove_field(0)
                value = f'出現 {advance - c} 秒前'
                exp = '\n 撃ち方用意！'if prenotice.get('boss') == 'ベル' else ''
                if advance == c:
                    value = '**出現！**{}'.format(exp)
                embed.add_field(name=prenotice.get('boss'),value=value)
                await msg.edit(embed=embed)
        self.reserved.remove(prenotice)
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop.start()
def setup(bot):
    bot.add_cog(Prenotice(bot))
