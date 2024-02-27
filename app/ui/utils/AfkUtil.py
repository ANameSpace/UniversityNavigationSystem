import time

from app.utils.tools.Log import Log


class AfkUtil:
    def __init__(self):
        self.last_time = time.time()
        self.changes = False

    def check_new_changes(self):
        current_time = time.time()

        if not self.changes:
            return False

        if current_time - self.last_time > 300:  # 5 min = 300 sec
            self.changes = False
            Log().send(Log.LogType.INFO, "Absence of actions in the last 5 minutes. Return to the initial window.")
            return True
        return False

    def action(self):
        self.changes = True
        self.last_time = time.time()
