from telethon import TelegramClient, events, errors
from data import *
from typing import Final
from cprint import *
import configparser
import logging
import asyncio
import sys
import os

data = {
    'id': int,
    'hash': str,
    'phone': str
}

_SLEEP_ASYNC: Final = 3
_TARGET_CHATS: Final = tuple(
    int(i.strip()) for i in open('../textfiles/messagebot/chat_target.txt', 'r').readlines()
)


cread = configparser.ConfigParser()
cread.read('../config.ini')
data['id'] = int(cread['UserInfo']['id'])
data['hash'] = cread['UserInfo']['hash']
data['phone'] = cread['UserInfo']['phone']

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

client = TelegramClient(data['phone'], data['id'], data['hash'])

triggers_responses = dict()
response_files = tuple(os.walk("../textfiles/responses"))[0][2]
if len(response_files) == 0:
    cprint.warn("Make sure you that responses folder is not empty")
    sys.exit(1)
for resp in response_files:
    if resp.startswith('response'):
        file = open(f"../textfiles/responses/{resp}", "r").readlines() 
        text = "".join(file).split('///')
        try:
            trigger, response = text[0].strip(), text[1]
            triggers_responses[trigger] = response
        except IndexError:
            cprint.err("Make sure that you read how to use response files")
            sys.exit(1)
    else:
        continue


@client.on(events.NewMessage(chats=_TARGET_CHATS))
async def reaction(event):
    await client.connect()
    for trig in triggers_responses.keys():
        if trig in str(event.raw_text).lower():
            sender = await event.get_sender()
            if not restricted(sender.id):
                await asyncio.sleep(_SLEEP_ASYNC)
                try:
                    await client.send_message(
                        sender.id, triggers_responses[str(trig).lower()]
                    )
                except errors.rpcbaseerrors.ForbiddenError:
                    cprint.warn(f"{sender.username if sender.username is not None else sender.id} "
                                f"blocked you :("
                                )
                finally:
                    add_restricted(sender.id)
            else:
                cprint.info(
                    f"{sender.username if sender.username is not None else sender.id} "
                    f"will not receive messages anymore :0"
                )


try:
    cur.execute("CREATE TABLE if NOT EXISTS restricted(id integer)")
    with client:
        client.run_until_disconnected()
except sqlite3.OperationalError:
    pass
except RuntimeError:
    pass
