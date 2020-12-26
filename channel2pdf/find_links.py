from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from data import *
import yaml
import asyncio

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

client = TelegramClient('session_file', credential['api_id'], credential['api_hash'])
client.start(password=credential['password'])


def findLinks(source):
    channel_entity=client.get_entity(source)
    posts = client(GetHistoryRequest(peer=channel_entity, limit=30, offset_date=None,
        offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
    print(asyncio(posts))