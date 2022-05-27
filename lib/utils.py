import datetime
import logging
import platform
import sys
import time

red = "\033[1;31m"
green = "\033[1;32m"
cyano = "\033[1;36m"
blue = "\033[94m"


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


def string_painter(string, beginning_color=None, ending_color=None):
    if platform.system() == "Windows":
        printed_string = string
    else:
        if beginning_color and ending_color:
            printed_string = beginning_color + string + ending_color
        elif beginning_color:
            printed_string = beginning_color + string
        elif ending_color:
            printed_string = string + ending_color
        else:
            printed_string = string

    return printed_string


def logMovedSuccess(toLog):
    logger_1.info(toLog)


def logMovedFailure(toLog):
    logger_2.info(toLog)


def logError(e):
    print(string_painter("EXCEPTION --> " + str(e), red))


def waitingAnimation(n):
    n = n % 3+1
    dots = n*'.'+(3-n)*' '
    sys.stdout.write('\r Waiting ' + dots)
    sys.stdout.flush()
    time.sleep(0.5)
    return n


def wait(sec):
    print(string_painter(f'Continue in {sec} seconds', cyano))
    for s in range(sec):
        waitingAnimation(s)
        time.sleep(0.5)


def user_activity_menu():
    print(string_painter("\nHow would you like to obtain the users?\n", green))
    print(string_painter("[0] All Users", red))
    print(string_painter("[1] Active Users (online today and yesterday)", red))
    print(string_painter("[2] Users active in the last week", red))
    print(string_painter("[3] Users active in the last month", red))
    print(string_painter("[4] Non-active users (non-active in the last month)", red))
    online_users_status = input(string_painter("\nEnter choise: ", green, red))

    return online_users_status


def define_user_filter(choise):
    if choise == 1:
        return user_filter1
    elif choise == 2:
        return user_filter2
    elif choise == 3:
        return user_filter3
    elif choise == 4:
        return user_filter4

    return user_filter0


def time_user_filter(user, seconds_time_delta=0):
    now = datetime.datetime.now()
    try:
        user_was_online = user.status.was_online
    except:
        if seconds_time_delta < 0:
            return True
        return False

    user_time_diff = now - user_was_online.replace(tzinfo=None)

    if seconds_time_delta < 0:
        if user_time_diff.seconds > abs(seconds_time_delta):
            return True
    elif seconds_time_delta == 0:
        return True
    elif user_time_diff.seconds < seconds_time_delta:
        return True
    return False


def user_filter0(user):
    return time_user_filter(user=user, seconds_time_delta=0)


def user_filter1(user):
    return time_user_filter(user=user, seconds_time_delta=172800)


def user_filter2(user):
    return time_user_filter(user=user, seconds_time_delta=604800)


def user_filter3(user):
    return time_user_filter(user=user, seconds_time_delta=2592000)


def user_filter4(user):
    return time_user_filter(user=user, seconds_time_delta=-2592000)
