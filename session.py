import configparser
import csv
import os
import sys
import time

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from utils import *


class Account:
    def __init__(self, nome, api_id, api_hash, phone, client):
        self.nome = nome
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = client
        self.channell = None

    def toString(self):
        return("Account "+self.nome)


cpass = configparser.RawConfigParser()
cpass.read('.config')
n = int(cpass['info']['n'])
accounts = [None]*n


def checkAuth(account):
    try:
        if not account.client.is_user_authorized():
            account.client.send_code_request(account.phone)
            account.client.sign_in(account.phone, input(
                gr+'Inserisci il codice ricevuto da '+account.nome+' su Telegram: '+cy))
        return True
    except Exception as e:
        logError(e)
        return False


def init():
    try:
        for i in range(n):
            cred = 'cred' + str(i)
            nome = cpass[cred]['nome']
            api_id = cpass[cred]['id']
            api_hash = cpass[cred]['hash']
            phone = cpass[cred]['phone']
            client = TelegramClient(phone, api_id, api_hash)
            client.connect()
            account = Account(nome, api_id, api_hash, phone, client)
            if checkAuth(account):
                accounts[i] = account
            else:
                print(re + "Client " + str(i+1) +
                      " ha fallito l'autenticazione!")
                return False
            print(gr + accounts[i].toString() + " autenticato!")
    except Exception as e:
        logError(e)
        return False
    return True
