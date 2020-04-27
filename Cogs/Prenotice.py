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
        self.json_data = []
        self.next_boss = []
        self.read_json('wb.json')
    def read_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        for read_schedule in self.json_data.get("schedule"):
            advances = self.json_data.get('advance')
            if 'advance' in read_schedule.keys():
                advances = read_schedule.get('advance')
            for advance in advances:
                schedule = read_schedule.copy()
                schedule["thumbnail"] = self.json_data.get("boss").get(schedule.get("boss"))
                schedule["advance"] = advance
                if schedule not in self.schedules:
                    self.schedules.append(schedule)
    @classmethod
    def next_prenotice_datetime(cls, now:datetime, prenotice):
        prenotice_time = datetime(now.year,
                            now.month,
                            now.day,
                            prenotice.get('hour'),
                            prenotice.get('minute'),
                            0)
        prenotice_time +=  timedelta(days=prenotice.get('weekday') - now.weekday())
        if prenotice_time - now < timedelta(0):
            prenotice_time += timedelta(days=7)
        if prenotice_time < now:
            logger.error(f"prenotice is past: {prenotice_time} < {now}")
        return prenotice_time

    @commands.command()
    async def prenotice(self, ctx):
        await self.do_loop()
        pass
    @tasks.loop(minutes=5)
    async def loop(self):
        await self.do_loop()
    async def do_loop(self):
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
        if not self.next_boss:
            now = datetime.now()
            logger.debug("into boss nxt")
            min_delta = min([self.next_prenotice_datetime(now, prenotice) - now for prenotice in self.json_data.get('schedule')])
            self.next_boss = [prenotice for prenotice in self.json_data.get('schedule') if self.next_prenotice_datetime(now, prenotice) - now == min_delta]
            for prenotice in self.next_boss:
                await self.set_next_boss(prenotice, min_delta.total_seconds())
            asyncio.sleep(min_delta.total_seconds())
            logger.debug("boss list clear")
            self.next_boss = []
    async def send_boss_prenotice(self, prenotice, delay:int):
        self.reserved.append(prenotice)
        logger.debug(f"{prenotice} is append reserved list")
        await asyncio.sleep(delay)
        channel = self.bot.get_channel(self.config.getint('prenotice_channel'))
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
    async def set_next_boss(self, prenotice, delete_after):
        channel = self.bot.get_channel(self.config.getint('next_boss_channel'))
        logger.debug(f"next boss channel: {channel.id}")
        logger.debug(f"delete_after: {delete_after}s, type: {type(delete_after)}")
        thumbnail = self.json_data.get("boss").get(prenotice.get("boss"))
        embed = discord.Embed(title="次ボス")
        embed.add_field(name=f"{prenotice.get('hour')} : {prenotice.get('minute')}", value=f"**{prenotice.get('boss')}**")
        embed.set_thumbnail(url=thumbnail)
        msg = await channel.send(embed=embed, delete_after=delete_after)
        pass
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop.start()
def setup(bot):
    bot.add_cog(Prenotice(bot))
