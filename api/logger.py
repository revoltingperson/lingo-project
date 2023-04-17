import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from os.path import exists

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

logFile = Path.joinpath(Path.cwd(), 'log_activity.txt')
if not exists(logFile):
    with open(logFile, 'w') as f:
        f.write('')

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=False)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)