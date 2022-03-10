import csv
import random
import sys

from telethon.errors.rpcerrorlist import (PeerFloodError,
                                          UserPrivacyRestrictedError)
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChannel, InputPeerEmpty, InputPeerUser

import session as s
from utils import *


class User:
    def __init__(self, username, id, access_hash, name):
        self.username = username
        self.id = id
        self.access_hash = access_hash
        self.name = name

    def toString(self):
        return (cy + 'Utente: ' + self.username + " | ID: " + str(self.id))


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
    print(cy + 'Numero account operativi: ' + str(s.n))
else:
    print(re + 'L\'inizializzazione degli account è fallita')
    exit(1)

try:
    print(cy+'Lettura del file: ' + sys.argv[1])
    input_file = sys.argv[1]
except Exception as e:
    logError(e)
    print(re+'Devi specificare il nome del file da cui prelevare gli account.')
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
    logError('Possibile errore nel CSV riga ' + str(count))
    logError(e)
    exit(1)

print(gr+'Lettura del file avvenuta con successo!')
print(cy + str(len(users)) + ' utenti da spostare\n')


print(cy+'ATTENZIONE!\nPer ogni Account va selezionato lo stesso gruppo.')
for a in s.accounts:
    print(cy+a.toString())
    i = 0
    groups = readGroups(a)
    for group in groups:
        print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
        i += 1

    print(cy+'Seleziona il gruppo a cui aggiungere gli utenti')
    g_index = input(cy+"Scegli un numero: ")
    target_group = groups[int(g_index)]
    a.channell = InputPeerChannel(target_group.id, target_group.access_hash)
    print(cy+'-----------------\n')

index = 0
count = 0

wait(10)

for user in users:
    count += 1
    if count > 20:
        index += 1
        if index == len(s.accounts):
            index = 0
        print(cy+"Cambio da " + account.toString() +
              " --> " + s.accounts[index].toString())
        count = 0
    print('Count: ' + str(count))
    account = s.accounts[index]
    client = account.client
    try:
        print(user.toString())
        if user.username == "":
            continue
        user_to_add = client.get_input_entity(user.username)
        #user_to_add = InputPeerUser(user.id, user.access_hash)
        client(InviteToChannelRequest(account.channell, [user_to_add]))
        logMovedSuccess(user.username)
        print(gr+"Utente aggiunto con successo! " + account.toString())
        wait(random.randrange(60, 65))
    except PeerFloodError as err:
        logMovedFailure(user.username)
        index += 1
        if index == len(s.accounts):
            index = 0
        print(re+"ATTENZIONE FLOOD ERROR!!!\nCambio da " +
              account.toString() + " --> " + s.accounts[index].toString())
        count == 0
        wait(900)
    except UserPrivacyRestrictedError as err:
        logMovedFailure(user.username)
        print(re+"Le impostazioni di privacy dell'utente non permettono l'aggiunta.")
        wait(random.randrange(60, 65))
    except Exception as err:
        logMovedFailure(user.username)
        print(re+"Errore non gestito.")
        logError(err)
        index += 1
        if index == len(s.accounts):
            index = 0
        print(cy+"Cambio da " + account.toString() +
              " --> " + s.accounts[index].toString())
        count == 0
        wait(random.randrange(60, 65))
    continue
