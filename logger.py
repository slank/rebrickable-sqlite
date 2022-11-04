import logging
import os

# DEFAULT_FMT = "(%(filename)s:%(lineno)d) %(message)s"
DEFAULT_FMT = "%(message)s"

class ColorLogFormatter(logging.Formatter):
    grey = "\x1b[37m"
    bold_grey = "\x1b[37;1m"
    blue = "\x1b[34;1m"
    yellow = "\x1b[33m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    @classmethod
    def format_levelname(cls, levelno, levelname):
        color = {
            logging.INFO: cls.blue,
            logging.WARNING: cls.yellow,
            logging.ERROR: cls.red,
            logging.CRITICAL: cls.bold_red,
        }.get(levelno, cls.grey)
        return "[" + color + levelname + cls.reset + "]"

    def format(self, record):
        morelines = []
        if "\n" in record.msg:
            record.msg, *morelines = record.msg.splitlines()
        message = super().format(record)
        prefix = self.format_levelname(record.levelno, record.levelname)
        output = prefix + " " + message
        for line in morelines:
            output += "\n...  " + line
        return output


def setupLogging(format=DEFAULT_FMT):
    log_level = logging.INFO
    if os.getenv("DEBUG"):
        log_level = logging.DEBUG
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(ColorLogFormatter(format))
    root.addHandler(handler)
