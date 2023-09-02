from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors.rpcerrorlist import ChannelPrivateError, ChatAdminRequiredError
from telethon.tl.types import InputPeerEmpty
from typing import Final
import configparser
from cprint import *
import sqlite3
import time
import csv
import sys
import os

_SLEEPING : Final = 3
data = dict()

try:
    cread = configparser.ConfigParser()
    cread.read('../config.ini')
    data['id'] = int(cread['UserInfo']['id'])
    data['hash'] = cread['UserInfo']['hash']
    data['phone'] = cread['UserInfo']['phone']
    client = TelegramClient(data['phone'], data['id'], data['hash'])
except KeyError:
    os.system('clear')
    cprint.err("// You need to run setup.py first!\n")
    sys.exit(1)

try:
    client.start()
    client.connect()
except sqlite3.OperationalError:
    cprint.err("// Unexpected error, run the script again")
    sys.exit(1)

chats = client(GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=200,
    hash=0
)).chats

groups = list()
for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except AttributeError:
        continue


for group_num in range(1, len(groups) + 1):
    print(f"[{group_num}] - {groups[group_num - 1].title}")

cprint.ok('// Choose a group to scrape members')
cprint.ok(35 * '↓')

try:
    group_index = int(input())
except ValueError:
    cprint.err("// Type in group number!")
    sys.exit(1)

try:
    target_group = groups[int(group_index) - 1]
    cprint.info('// Fetching members...')
    time.sleep(_SLEEPING)
except IndexError:
    cprint.err("// Type in a real group number!")
    sys.exit(1)

try:
    all_participants = ([
        *client.get_participants(target_group, aggressive=True)
    ])
except ChannelPrivateError:
    cprint.err(f"// You have no access {target_group}. Try another one")
    sys.exit(1)
except ChatAdminRequiredError as error:
    cprint.err(error)
    sys.exit(1)

time.sleep(_SLEEPING)

with open("../members.csv", "w", encoding='UTF-8') as file:
    writer = csv.writer(file, delimiter=",", lineterminator="\n")
    writer.writerow(
        ['username', 'user id', 'access hash', 'name', 'group', 'phone']
    )

    for user in all_participants:
        username = user.username if user.username else ""
        first_name = user.first_name if user.username else ""
        last_name = user.last_name if user.last_name else ""
        name = f"{first_name} {last_name}".strip()
        phone = user.phone if user.phone else ""
        row = [username, user.id, user.access_hash, name, target_group.title, phone]
        writer.writerow(row)


if os.path.getsize('./members.csv') > 46:
    cprint.info('// Members scraped successfully.')
else:
    cprint.warn('// Probably you dont have enough rights to see members of the group')
