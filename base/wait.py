

from datetime import datetime
# from sqlite3 import Timestamp
import threading
import time

def time_expire_remove(queue, key, timelimit, starttime):
    time.sleep(timelimit)
    if key in queue and queue[key]['timestamp'] - starttime >= 599:
        queue.pop(key)

class ToBeVerified(dict):
    def __init__(self):
        self.tobeverified = {}

    def add(self,key, userobjs, timestamp):
        timestamp = max(600, timestamp)
        self.tobeverified[key] = userobjs
        self.tobeverified[key]['timestamp'] = timestamp
        t = threading.Thread(target=time_expire_remove, args=(self, key, timestamp, time.time()))
        t.start()

    def get(self, key):
        if key in self.tobeverified:
            return self.tobeverified[key]
        return None
toBeVerified = ToBeVerified()