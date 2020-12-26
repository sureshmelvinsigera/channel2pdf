from telethon import TelegramClient
from data import *
import yaml

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

client = TelegramClient('session_file', credential['api_id'], credential['api_hash'])
client.start(password=credential['password'])


def findLinks(source):
	peer = app.resolve_peer(-1001386704220)
	app.send(
            Search(
                peer=self.peer,
                q='',
                filter=InputMessagesFilterEmpty(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0,
                from_id=InputPeerSelf()
            )
        )
	last_msg_id = last_msg.get(source) or 1
	links = {}
	for msg_id in range(last_msg_id + 1, last_msg_id + 50):
		r = getLink(webgram.getPost(source, msg_id))
		if not r:
			continue
		last_msg.update(source, msg_id)
		links[r[0]] = r[1]
	for msg_id in range(last_msg_id, last_msg_id - 50, -1):
		if len(links) > 10:
			return links
		r = getLink(webgram.getPost(source, msg_id))
		if not r:
			continue
		links[r[0]] = r[1]
	return links