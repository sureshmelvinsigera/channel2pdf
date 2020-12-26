from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import yaml
import asyncio

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient('session_file', credential['api_id'], credential['api_hash'])
client.start(password=credential['password'])

async def findLinksAsync(source):
    channel_entity=await client.get_entity(source)
    posts = await client(GetHistoryRequest(peer=channel_entity, limit=30, # change to 30
        offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
    return posts

def findLinks(source):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r = loop.run_until_complete(findLinksAsync(source))
    links = {}
    for message in r.messages:
        try:
            message.media.webpage
        except:
            continue
        links[tuple([item.url for item in message.entities])] = (
            message.media.webpage.title[11:-21]).strip()
    return links
    