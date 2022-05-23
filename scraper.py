import csv
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

import session as s
from utils import *

if s.init():
    print(string_painter('Number of operative accounts: ' + str(s.n), cyano))
else:
    print(string_painter('User initialization failed', red))
    exit(1)

chats = []
last_date = None
chunk_size = 200
groups = []


def readGroups(account):
    groups = []
    chats = []
    last_date = None
    chunk_size = 200
    result = account.client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue
    return groups


print(string_painter('Choose a group to scrape members :', green, red))
i = 0
groups = readGroups(s.accounts[0])
for group in groups:
    print(string_painter('[' + str(i) + '] - ' + group.title, green, cyano))
    i += 1

g_index = input(string_painter("\nEnter a Number: ", green, red))
target_group = groups[int(g_index)]


if target_group.participants_count > 5000:
    print(string_painter(f"\n{target_group.title} group has more than 5000 users!", red))
    decision = input(string_painter("This could lead to an error, do you want to continue? [y/N] ", red))
    if decision == 'y':
        pass
    else:
        exit()

online_users_status = user_activity_menu()
while True:
    try:
        check = int(online_users_status)
        if check < 5:
            break
    except:
        pass
    print(string_painter("Invalid choise! You have to pick up a number between 0 and 4.", red))
    online_users_status = user_activity_menu()

user_filter = define_user_filter(int(online_users_status))

print(string_painter('Fetching Members...', green))
time.sleep(1)

#all_participants = s.accounts[0].client.iter_participants(entity=target_group)

all_participants = s.accounts[0].client.get_participants(target_group, aggressive=False)

print(string_painter('Saving In file...', green))
time.sleep(1)
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash',
                    'name', 'group', 'group id'])
    for user in all_participants:
        if user_filter(user):
            if user.username:
                username = user.username
            else:
                continue
                #username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash,
                            name, target_group.title, target_group.id])

print(string_painter(f'{all_participants.total} members scraped successfully.', green))
