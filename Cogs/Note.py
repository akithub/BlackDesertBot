from discord.ext import commands

import discord
import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)

class Note(commands.Cog):
    def __init__(self, bot):
        self.config = bot.get_cog('Config').config['MEMO']
        self.db = Database(self.config.get('DatabaseName'), self.config.get('collection'))
        pass

    @commands.command(aliases=['n'])
    async def note_look(self, ctx, *args):
        if not args:
            ctx.send('メモのタイトルを入れて？')
        result = self.db.find(args[0])
        if not result.count():
            await ctx.send("そんなもの知らないよ")
            result = self.db.find_re(args[0])
            if result.count():
                content = '\n'.join([f"{d.get('title')}" for d in result])
                await ctx.send("この辺にない？\n" +"-"*20 + "\n" + content)
            return
        await ctx.send(f"{result[0].get('content')}")

    @commands.group()
    async def note(self, ctx):
    # async def memo(self, ctx):
        logger.debug("memo is invoked")
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid memo command')
    @note.command(aliases=['a'])
    async def add(self, ctx, title:str, content:str, tags:str=''):
        logger.debug("memo add is invoked")
        res = self.db.find(title)
        if res.count():
            await ctx.send('すでに登録されてるよ')
            return
        res = self.db.add(title, content, tags)
        await ctx.send('書き込んだよ' if res else '書き込みに失敗したよ')
    @note.command(aliases=['t'])
    async def tag(self, ctx, tag):
        logger.debug("memo tag is invoked")
        result = self.db.find_tags(tag)
        if not result.count():
            await ctx.send("そんなタグないよ")
            return
        content = '\n'.join([f"{d.get('title')}: {d.get('content')}" for d in result])
        await ctx.send(content)
    @note.command()
    async def replace(self, ctx, title:str, content:str, tags:str=''):
        logger.debug("memo replace is invoked")
        res = self.db.find_one_and_replace(title, content, tags)
        await ctx.send('置き換えたよ')
    @note.command()
    async def all(self, ctx):
        logger.debug("memo all is invoked")
        result = self.db.find_all()
        if not result.count():
            await ctx.send('何も登録されてないよ')
            return
        content = '\n'.join([f"{d.get('title')}: {d.get('content')}" + f"(tag: {d.get('tags')})" for d in result])
        await ctx.send(content)
    @note.command(aliases=['d', 'del'])
    async def delete(self, ctx, title:str):
        logger.debug("memo delete is invoked")
        res = self.db.delete(title)
        if res.deleted_count:
            await ctx.send('消したよ')
    @note.command()
    async def reset(self, ctx):
        self.db.reset()
        await ctx.send('消したよ、全部')
    # @commands.command()
    # async def memo(self, ctx, title:str):
    #     result = self.db.find(title)
    #     if not result:
    #         await ctx.message.channel.send("そんなもの知らないよ")
    #         return
    #     await ctx.message.channel.send(f"{result['content']}")

class Database(object):
    def __init__(self, db_name, collection_name):
        self.db = MongoDB(db_name)
        self.collection_name = collection_name
    def add(self, title:str, content:str, tags:str):
        tags = tags.split(',')
        doc = {'title': title, 'content': content, 'tags': tags}
        result = self.db.insert(self.collection_name, doc)
        return result.acknowledged
    def find_one_and_replace(self, title:str, content:str, tags:str):
        tags = tags.split(',')
        doc = {'title': title, 'content': content, 'tags': tags}
        find_filter = {'title': title}
        result = self.db.find_one_and_replace(self.collection_name, find_filter, doc)
        return result
    def find(self, title:str):
        find_filter = {'title': title}
        result = self.db.find(self.collection_name, find_filter)
        return result
    def find_tags(self, tag:str):
        find_filter = {'tags': tag}
        result = self.db.find(self.collection_name, find_filter)
        return result
    def find_all(self):
        find_filter = {}
        result = self.db.find(self.collection_name, find_filter)
        return result
    def find_re(self, title:str):
        find_filter = {'title': {'$regex': title}}
        result = self.db.find(self.collection_name, find_filter)
        return result
    def delete(self, title:str):
        find_filter = {'title': title}
        result = self.db.delete_one(self.collection_name, find_filter)
        return result
    def reset(self):
        self.db.reset(self.collection_name)

class MongoDB(object):
    def __init__(self, db_name:str):
        self.client = MongoClient()
        self.db = self.client.get_database(db_name)
    def insert(self, collection_name:str, doc:dict):
        collection = self.db.get_collection(collection_name)
        logger.debug("doc : {}".format(collection))
        return collection.insert_one(doc)
    def find_one_and_replace(self, collection_name:str, find_filter:dict, doc:dict):
        collection = self.db.get_collection(collection_name)
        result = collection.find_one_and_replace(find_filter, doc)
        # logger.debug(f'replace: before: {result}')
    def delete_one(self, collection_name:str, find_filter:dict):
        collection = self.db.get_collection(collection_name)
        result = collection.delete_one(find_filter)
        return result
    def find(self, collection_name:str, find_filter:dict)->[dict]:
        collection = self.db.get_collection(collection_name)
        logger.debug("found count: {}".format(collection.find(find_filter).count()))
        return collection.find(find_filter, {'_id':0})
    def reset(self, table:str):
        collection = self.db.get_collection(table)
        collection.drop()

def setup(bot):
    bot.add_cog(Note(bot))