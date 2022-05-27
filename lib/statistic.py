from datetime import datetime

from utils import *


class Try:
    def __init__(self, username, time):
        self.username = username
        self.time = time


positiveTries = []
negativeTries = []

setup_logger('stats', "stats.log")
stats_logger = logging.getLogger('stats')


def positive(username):
    t = Try(username, datetime.now())
    positiveTries.append(t)


def negative(username):
    t = Try(username, datetime.now())
    positiveTries.append(t)
