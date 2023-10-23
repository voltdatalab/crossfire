from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    StreamHandler,
    getLogger,
)
from os import getenv
from sys import stderr

LEVELS = {
    "CRITICAL": CRITICAL,
    "DEBUG": DEBUG,
    "ERROR": ERROR,
    "INFO": INFO,
    "WARNING": WARNING,
}


class Logger:
    def __init__(self, name):
        self.logger = getLogger(name)

        if getenv("DEBUG"):
            self.logger.setLevel(DEBUG)
        elif level := LEVELS.get(getenv("LOG_LEVEL")):
            self.logger.setLevel(level)
        else:
            self.logger.setLevel(INFO)

        formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        out = StreamHandler()
        out.setLevel(DEBUG)
        out.setFormatter(formatter)
        self.logger.addHandler(out)

        err = StreamHandler(stream=stderr)
        err.setLevel(ERROR)
        err.setFormatter(formatter)
        self.logger.addHandler(err)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
