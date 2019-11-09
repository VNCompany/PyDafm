import time
from defines import *


class LogManager:
    def __init__(self):
        self.file = open("log.txt", "a", encoding="utf-8")

    def append(self, err_type: str, err_msg: str):
        dt = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        result = "[{0}][{1}]: {2} \n".format(dt, err_type, err_msg.replace("\n", " "))
        self.file.write(result)

    def close(self):
        self.file.close()


lm = LogManager()
lm.append(LOG_ERROR, "You are person!")
lm.append(LOG_INFORMATION, "You are person!")
lm.append(LOG_WARNING, "You are person!")
lm.close()
