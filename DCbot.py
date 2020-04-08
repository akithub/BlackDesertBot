from discord.ext import commands
import discord

import os
from configparser import ConfigParser
import argparse

import logging
import logging.handlers
from logging import getLogger, Filter, DEBUG, INFO

import ConfigCog
from Cogs import *

logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

config_parser = ConfigParser()
config_parser.optionxform = str

if not os.path.isfile('config.ini'):
    config_parser['DEFAULT'] = {
        'token': '',
        'guild_id': '',
        'DebugMode' : 'no',
        'DatabaseName' : 'discord_bot',
        'LogOutPath' : 'log/',
        'LogRootLevel' : 'info',
        'LogFileLevel' : 'info',
        'LogStreamLevel' : 'warning',
        'LogFileRotateCount' : 30,
    }
    config_parser['DEBUG'] = {
        'DebugMode' : 'yes',
        'DatabaseName' : 'test',
        'LogRootLevel' : 'debug',
        'LogFileLevel' : 'debug',
        'LogStreamLevel' : 'debug',
        'LogFileRotateCount' : 3,
    }
    config_parser['VOICE_INOUT'] = {
        'output_channel_id': '',
        'voice_channel_id': '',
    }
    with open('config.ini', 'w') as configfile:
        config_parser.write(configfile)

config_parser.read('config.ini')
config = config_parser['DEBUG'] if args.debug else config_parser['DEFAULT']
LOG_PATH    = config.get('LogOutPath')
ROOT_LEVEL  = config.get('LogRootLevel').upper()
STREAM_LEVEL = config.get('LogStreamLevel').upper()
FILE_LEVEL  = config.get('LogFileLevel').upper()
DATE_FORMAT  = '%y-%m-%d %H:%M:%S'
FORMAT       = '[%(asctime)s] {file_info}[%(levelname)-6s]: %(message)s'.format(file_info='%(name)15s:%(lineno)4s::%(funcName)20s() 'if ROOT_LEVEL == 'DEBUG' else '')
# stream
if STREAM_LEVEL != 'NONE':
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    handler.setLevel(STREAM_LEVEL)
    logger.addHandler(handler)
# file
if FILE_LEVEL != 'NONE':
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    # all
    handler = logging.handlers.TimedRotatingFileHandler(os.path.join(LOG_PATH, 'all.log'), when='MIDNIGHT', backupCount=config.getint('LogFileRotateCount'))
    handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    handler.setLevel(FILE_LEVEL)
    logger.addHandler(handler)
    # only app module
    handler = logging.handlers.TimedRotatingFileHandler(os.path.join(LOG_PATH, 'cogs.log'), when='MIDNIGHT', backupCount=config.getint('LogFileRotateCount'))
    handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    handler.setLevel(FILE_LEVEL)
    handler.addFilter(Filter('Cogs'))
    logger.addHandler(handler)
logger.setLevel(ROOT_LEVEL)

class DCbot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.load_extension('ConfigCog')
        self.get_cog('Config').config = config_parser
        self.load_extension('Cogs.Kujira')
        self.load_extension('Cogs.VCinout')

    async def on_ready(self):
        # print('Logged on as {{0}} (ID: {{0.id}})'.format(self.user))
        print('bot ready')
        logger.info('bot ready')

if __name__ == '__main__':
    client = DCbot(command_prefix='+')
    token =  config.get('token')
    client.run(token)