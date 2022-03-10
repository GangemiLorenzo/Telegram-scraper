import logging
import os
import time

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


setup_logger('log1', "moved.log")
setup_logger('log2', "not_moved.log")
logger_1 = logging.getLogger('log1')
logger_2 = logging.getLogger('log2')


def logMovedSuccess(toLog):
    logger_1.info(toLog)


def logMovedFailure(toLog):
    logger_2.info(toLog)


def logError(e):
    print(re + "EXCEPTION --> " + str(e))


def wait(sec):
    for s in range(sec):
        print(cy + 'Continua in ' + str(sec-s) + ' ...')
        time.sleep(1)
    os.system('clear')
