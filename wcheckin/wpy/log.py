import atexit
import logging
import os
import shutil
import sys
from datetime import datetime
from os import mkdir
from os import path
from tkinter import messagebox

logging_file_name: str = ''


def _exit_handler():
    _archive_log()
    global logging_file_name
    with open(logging_file_name) as f:
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            lines = f.read().split('\n')
            lines = [x[0:41] for x in lines]
            text = '\n'.join(lines)
            import webbrowser
            url = "file://" + os.getcwd() + '/' + logging_file_name
            webbrowser.open(url)
        else:
            print(f.read())


def _archive_log():
    archive_dir = './logs-publish-and-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    global logging_file_name
    dt = str(datetime.now())
    sfx = ',' + dt[5:10] + '.log'
    archived_name = logging_file_name.replace('.log', sfx)
    log_archive_file = archive_dir + '/' + archived_name
    print('logging_file_name=',logging_file_name)
    print('log_archive_file=',log_archive_file)
    import os
    print(os.getcwd())
    shutil.copyfile(logging_file_name, log_archive_file)


def config_log(file_name):
    global logging_file_name
    logging_file_name = file_name
    if len(sys.argv) == 1:
        log_level = logging.INFO
        log_format = '%(message)s'
    else:
        log_level = logging.DEBUG
        # log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
        log_format = '[%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
    logging.basicConfig(filename=logging_file_name, filemode='w', level=log_level, format=log_format)
    logging.info(str(datetime.now()))
    logging.info('log config done; log file: '+file_name)
    atexit.register(_exit_handler)
