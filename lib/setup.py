import os
import platform
import subprocess
import sys

from constants import CONFIG, REQUIREMENTS
from utils import *


def banner():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system('clear')
    print("""
    Welcome within the telegram scraper installation 
    """)


def requirements():
    banner()
    print(string_painter("> I'm installing the dependencies ...", red))
    if platform.system() == "Windows":
        py_path = "python3"
    else:
        if os.environ.get("VIRTUAL_ENV"):
            py_path = os.path.join(os.environ.get("VIRTUAL_ENV"), "python3")
        else:
            py_path = "python3"

    subprocess.call(f"{py_path} -m pip install -r {REQUIREMENTS}", shell=True)
    #banner()
    #print(string_painter("> I'm installing the dependencies ...", red))
    print(string_painter("> Dependencies have been installed.\n", red))


def config_setup():
    import configparser
    cpass = configparser.RawConfigParser()
    cpass.add_section('info')
    n = input(string_painter("> How many account do you want to configure: ", green, cyano))
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
        xnome = input(string_painter("> Provide NAME: ", green, cyano))
        cpass.set(cred, 'nome', xnome)
        xid = input(string_painter("> Provide ID: ", green, cyano))
        cpass.set(cred, 'id', xid)
        xhash = input(string_painter("> Provide HASH: ", green, cyano))
        cpass.set(cred, 'hash', xhash)
        xphone = input(string_painter("> Provide phone number: ", green, cyano))
        cpass.set(cred, 'phone', xphone)
        setup = open(CONFIG, 'w')
        cpass.write(setup)
    setup.close()
    print(string_painter("> Saved credentials.", red))


def help():
    print(string_painter("""$ python3 setup.py -m file1.csv file2.csv

    ( --config  / -c ) Allows to configure the accounts
    ( --install / -i ) Install the dependecies
    ( --help    / -h ) Show this message
        """), green)


try:
    if any([sys.argv[1] == '--config', sys.argv[1] == '-c']):
        config_setup()
    elif any([sys.argv[1] == '--install', sys.argv[1] == '-i']):
        requirements()
    elif any([sys.argv[1] == '--help', sys.argv[1] == '-h']):
        help()
    else:

        print(string_painter('\nThe provided argument is not supported: ' + sys.argv[1], red))
        print(string_painter('If you need help use: ', green))
        print('$ python3 setup.py -h')
except IndexError:
    print(string_painter('No argument provided.', red))
    print(string_painter('If you need help use: ', green))
    print('$ python3 setup.py -h')
