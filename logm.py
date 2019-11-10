import time


class LogManager:
    def __init__(self):
        self.file = open("log.txt", "a", encoding="utf-8")

    def append(self, err_type: str, err_msg: str):
        dt = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        result = "[{0}][{1}]: {2} \n".format(dt, err_type, err_msg.replace("\n", " "))
        self.file.write(result)

    def close(self):
        self.file.close()
