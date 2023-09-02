from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputChannel, InputUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from cprint import *
from typing import Final
import configparser
import csv
import os
import time


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
    cprint.err("You need to run setup.py first!\n")
    sys.exit(1)


client.connect()
groups = []

chats = client(GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=200,
    hash=0
)).chats


for chat in chats:
    try:
        if chat:
            groups.append(chat)
    except AttributeError:
        continue


for group_num in range(1, len(groups) + 1):
    print(f"[{group_num}] - {groups[group_num - 1].title}")

cprint.ok('// Choose a group to invite members')
cprint.ok(35 * '↓')

try:
    group_index = int(input())
except ValueError:
    cprint.err("// Type in group number!")
    sys.exit(1)


try:
    target_group = groups[int(group_index) - 1]
    cprint.info('// Processing...')
    time.sleep(_SLEEPING)
except IndexError:
    cprint.err("File not found!")
    sys.exit(1)

cprint.ok("// By default you invite people from members.csv")
cprint.ok("// Do you want to change it? [0-no/1-yes]")
cprint.ok(25 * '↓')

file = ""

if choice := int(input()) == 1:
    cprint.ok("// Type in the file")
    cprint.ok('↓' * 19)
    file = input()
    try:
        if file.endswith(".csv"):
            cprint.ok("// Looking for a file...")
        else:
            cprint.err("// Only csv file is acceptable")
            sys.exit(1)
    except FileNotFoundError:
        cprint.err("// Make sure your csv file is in the same directory")
        sys.exit(1)
elif choice == 0:
    cprint.ok("// OK!")
else:
    cprint.err("// Error: type in 0 or 1")
    sys.exit(1)

cprint.info("// Staring the script... ")


def get_users(input_file):
    default_file = "../members.csv"
    if input_file != "":
        default_file = input_file
    with open(default_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        try:
            for row in rows:
                yield {
                    'username' : row[0],
                    'id' : int(row[1]),
                    'access_hash' : int(row[2]),
                    'name' : row[3],
                    'group' : row[4],
                    'phone' : row[5]
                }
        except ValueError:
            cprint.err("// Make sure you have the same fields in your csv file")
            sys.exit(1)


target_group_entity = InputChannel(target_group.id, target_group.access_hash)


async def invitation():
    for user in get_users(file):
        try:
            print(f"// Adding {user['username'] if user['username'] else user['id']}")
            time.sleep(5)
            user_to_add = InputUser(
                user_id=user['id'], access_hash=user['access_hash']
            )
            await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        except PeerFloodError:
            cprint.warn(
                "// Getting Flood Error from telegram. \n"
                "// Script is stopping now. \n"
                "// Please try again after some time."
            )
            sys.exit(1)
        except UserPrivacyRestrictedError:
            cprint.warn(
                f"// The {user['username'] if user['username'] else user['id']} "
                f"privacy settings do not allow you to do this. Skipping."
            )


with client:
    client.loop.run_until_complete(invitation()) 
    client.disconnect()
