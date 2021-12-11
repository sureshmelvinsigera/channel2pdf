#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html_telegraph_poster import TelegraphPoster
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import yaml
import asyncio

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

async def get_entity(client, source):
    credential['id_map'] = credential.get('id_map', {})
    if source not in credential['id_map']:
        entity = await client.get_entity(source)
        credential['id_map'][source] = entity.id
        with open('credential', 'w') as f:
            f.write(yaml.dump(credential, sort_keys=True, indent=2, allow_unicode=True))
    return await client.get_entity(credential['id_map'][source])

async def findMessages(channel_id, start_index):
    client = TelegramClient('session_file', credential['api_id'], credential['api_hash'])
    await client.start(password=credential['password'])
    await client.get_dialogs()
    channel_entity=await get_entity(client, channel_id)
    messages = []
    for i in range(3):
        posts = await client(GetHistoryRequest(peer=channel_entity, limit=100,
            offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=start + i * 100, hash=0))
        messages += post.messages
    await client.disconnect()
    return channel_entity, messages

def getList(db):
    real_index = 0
    while real_index < len(db):
        raw += 1
        if raw not in db:
            continue
        brief, link = db[raw]
        real_index += 1
        posts.append(
            '<p>%d. <a href="%s">%s</a></p>' % 
            (real_index, link, brief))
    return ''.join(posts)

def post(source, db):
    p = TelegraphPoster()
    if source.username:
        author_url = 'https://t.me/' + source.username
    else:
        author_url = None
    content = getList(db)
    text = '''  
<div>
    <p><strong>【频道简介】</strong></p>
    <p>%s</p>
    <p><a href="%s">点此进入频道</a></p>
    <br/>
    <p><strong>【索引】</strong></p>
    %s
</div>
    ''' % (source.description.split()[0], author_url, content)
    r = p.post(
        title = '【频道手册】%s ' % source.title,
        author = source.title, 
        author_url = author_url,
        text = text)
    return r['url']

def genIndex(channel_id, start_index):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    channel, messages = loop.run_until_complete(findMessages(channel_id, start_index))
    loop.close()
    print(channel)
    for message in messages:
        print(message)
        print(message.media.file)
        print(message.file)
        db[message.message_id] = '1', 'https://t.me/%s/%d' % (channel.username, message_id)
    post(source, db)