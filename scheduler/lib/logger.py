import logging
from enum import Enum
import traceback
from pathlib import Path


class LogType(Enum):
    strategy = 0
    operational = 1


try:
    logger = logging.getLogger('trade Logger')
    file = logging.FileHandler(Path('logs/log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file.setFormatter(formatter)
    logger.addHandler(file)
    logger.setLevel(logging.INFO)

except Exception as e:
    print("error loading logger: ", e)


def log_msg(msg):  # logType should be an int so we dont have to import LogType everywhere
    try:
        print(msg)
        logger.info(msg)
    except Exception as e:
        print("couldnt log to file: ", e)


def log_exception(functionName):
    if 'KeyboardInterrupt' in traceback.format_exc():
        print('Keyboard interrupt failed to exit...')
        return
    msg = f"Exception @ {functionName} : {traceback.format_exc()}"
    print(msg)
    logger.error(msg)
