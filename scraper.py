import csv
import time

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

import session as s
from utils import *

if s.init():
    print(cy + 'Numero account operativi: ' + str(s.n))
else:
    print(re + 'L\'inizializzazione degli account è fallita')
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


print(gr+'[+] Choose a group to scrape members :'+re)
i = 0
groups = readGroups(s.accounts[0])
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
    i += 1

print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group = groups[int(g_index)]

print(gr+'[+] Fetching Members...')
time.sleep(1)
all_participants = []
all_participants = s.accounts[0].client.get_participants(
    target_group, aggressive=True)

print(gr+'[+] Saving In file...')
time.sleep(1)
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash',
                    'name', 'group', 'group id'])
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
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
print(gr+'[+] Members scraped successfully.')
