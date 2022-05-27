import csv
import os
import random
import sys

from telethon.errors.rpcerrorlist import (PeerFloodError,
                                          UserPrivacyRestrictedError)
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChannel, InputPeerEmpty, InputPeerUser

import session as s
from preferences import (FLOOD_ERROR_DELAY, MAX_USERS_MOVED,
                         adding_error_delay, user_add_delay)
from utils import *


class User:
    def __init__(self, username, id, access_hash, name):
        self.username = username
        self.id = id
        self.access_hash = access_hash
        self.name = name

    def toString(self):
        return (string_painter('User: ' + self.username + " | ID: " + str(self.id), cyano))


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


if s.init():
    print(string_painter('Number of operative accounts: ' + str(s.n), cyano))
else:
    print(string_painter('User initialization failed', red))
    exit(1)

try:
    if os.path.exists("./members.csv") and len(sys.argv) == 1:
        sys.argv.append("./members.csv")
    print(string_painter('File reading: ' + sys.argv[1], cyano))
    input_file = sys.argv[1]
except Exception as e:
    logError(e)
    print(string_painter('You must specify the filename containing the users to add.', red))
    exit(1)

users = []
count = 1
try:
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            count += 1
            user = User(row[0], int(row[1]), int(row[2]), row[3])
            users.append(user)
except Exception as e:
    logError('Possible errors within the CSV row ' + str(count))
    logError(e)
    exit(1)

print(string_painter('Successful file reading!', green))
print(string_painter(str(len(users)) + ' users to move\n', cyano))


print(string_painter('PAY ATTENTION!\nFor each account the same group must be selected.', cyano))
for a in s.accounts:
    print(string_painter(a.toString(), cyano))
    i = 0
    groups = readGroups(a)
    for group in groups:
        print(string_painter("[" + str(i) + "]" + ' - ' + group.title, green, cyano))
        i += 1

    print(string_painter('Select the group where the users have to be added', cyano))
    g_index = input(string_painter("Choose a number: ", cyano))
    target_group = groups[int(g_index)]
    a.channell = InputPeerChannel(target_group.id, target_group.access_hash)
    print(string_painter('-----------------\n', cyano))

index = 0
count = 0

wait(2)

for user in users:
    count += 1
    if count > MAX_USERS_MOVED:
        index += 1
        if index == len(s.accounts):
            index = 0
        print(string_painter("\nChanging from " + account.toString() +
              " --> " + s.accounts[index].toString(), cyano))
        count = 0
    print('Count: ' + str(count))
    account = s.accounts[index]
    client = account.client
    try:
        print(user.toString())
        if user.username == "":
            continue
        user_to_add = client.get_input_entity(user.username)
        #user_to_add = InputPeerUser(user.id, client.get_entity(user.id).access_hash)
        client(InviteToChannelRequest(account.channell, [user_to_add]))
        logMovedSuccess(user.username)
        print(string_painter("User added successfully! " + account.toString(), green))
        wait(random.randrange(user_add_delay["min"], user_add_delay["max"]))
    except PeerFloodError as err:
        logMovedFailure(user.username)
        index += 1
        if index == len(s.accounts):
            index = 0
        print(string_painter("ATTENZION FLOOD ERROR!!!\nSwitch from " +
              account.toString() + " --> " + s.accounts[index].toString(), red))
        count = 0
        wait(FLOOD_ERROR_DELAY)
    except UserPrivacyRestrictedError as err:
        logMovedFailure(user.username)
        print(string_painter("The user privacy setting prevents from adding him/her to the group.", red))
        wait(random.randrange(adding_error_delay["min"], adding_error_delay["max"]))
    except Exception as err:
        logMovedFailure(user.username)
        print(string_painter("Unmanaged error.", red))
        logError(err)
        index += 1
        if index == len(s.accounts):
            index = 0
        print(string_painter("Switch from " + account.toString() +
              " --> " + s.accounts[index].toString(), cyano))
        count = 0
        wait(random.randrange(adding_error_delay["min"], adding_error_delay["max"]))
    continue
