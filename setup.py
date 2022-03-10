import os
import sys
import time

from utils import *


def banner():
    os.system('clear')
    print(f"""
	{re}Benvenuto nell'installazione di telegram scraper 
	""")


def requirements():
    banner()
    print(re+"> Sto installando le dipendenze ...")
    os.system("""
		pip3 install telethon requests configpars
		python3 -m pip install telethon requests configparser
		""")
    banner()
    print(re+"> Sto installando le dipendenze ...")
    print(re+"> Le dipendenze sono state installate.\n")


def config_setup():
    import configparser
    cpass = configparser.RawConfigParser()
    cpass.add_section('info')
    n = input(gr+"> Quanti account vuoi configurare: "+cy)
    if not n.isnumeric():
        config_setup()
        return
    n = int(n)
    if n < 1:
        config_setup()
        return
    cpass.set('info', 'n', n)
    for i in range(n):
        print("> Account n." + str(i+1))
        cred = 'cred' + str(i)
        cpass.add_section(cred)
        xnome = input(gr+"> Inserisci il NOME: "+cy)
        cpass.set(cred, 'nome', xnome)
        xid = input(gr+"> Inserisci l'ID: "+cy)
        cpass.set(cred, 'id', xid)
        xhash = input(gr+"> Inserisci l'HASH: "+cy)
        cpass.set(cred, 'hash', xhash)
        xphone = input(gr+"> Inserisci il numero di telefono: "+cy)
        cpass.set(cred, 'phone', xphone)
        setup = open('.config', 'w')
        cpass.write(setup)
    setup.close()
    print(re+"> Credenziali salvate.")


def help():
    print(gr+"""$ python3 setup.py -m file1.csv file2.csv

	( --config  / -c ) Permette di configurare gli account
	( --install / -i ) Installa le dipendenze
	( --help    / -h ) Mostra questo messaggio
			""")


try:
    if any([sys.argv[1] == '--config', sys.argv[1] == '-c']):
        config_setup()
    elif any([sys.argv[1] == '--install', sys.argv[1] == '-i']):
        requirements()
    elif any([sys.argv[1] == '--help', sys.argv[1] == '-h']):
        help()
    else:
        print(re+'\nArgomento non supportato : ' + sys.argv[1])
        print(gr+'Per aiuto utilizza: ')
        print('$ python3 setup.py -h')
except IndexError:
    print(re+'Nessun argomento specificato.')
    print(gr+'Per aiuto utilizza: ')
    print('$ python3 setup.py -h')
