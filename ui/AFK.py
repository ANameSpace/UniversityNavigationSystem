import time

from utils.Log import Log

last_time = time.time()


def check_time():
    current_time = time.time()
    if current_time - last_time > 300:  # 5 min = 300 sec
        Log().send(Log.LogType.INFO, "Absence of actions in the last 5 minutes. Return to the initial window.")
        return True
    return False


def action():
    global last_time
    last_time = time.time()
