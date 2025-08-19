from logger import Logger

class Backup:
    def __init__(self, interval = 600):
        Logger.info("Backups ready!")
        self.interval = interval
