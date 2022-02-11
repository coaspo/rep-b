import datetime
import json
import logging
import logging.handlers
import os
import traceback

log = logging.getLogger(__name__)
non_letters_regex = ''.join(['|\\' + x for x in r'[\^$.|?*+()'])  # regex special char's
non_letters_regex = non_letters_regex + ''.join(['|\\' + x for x in ',!@#$%&-_=:;"?<>/{}]]'])  # other non-ltr char's
NON_LETTERS_REGEX = '\'|[0-9]+' + non_letters_regex


class Config(dict):
    TRANSLATE_INSTRUCTIONS = 'Enter text on left panel and click Translate. \
    To change the default language in the combo boxes, edit ltrans/config_ltrans.json.'
    SAVE_INSTRUCTIONS = 'May change any text and add comments before clicking Save.'

    def __init__(self, config_file_path=None, **kw):
        if config_file_path is not None and kw != {}:
            raise Exception('ambiguous constructor arg - use file path or dict arg\'s')

        if config_file_path == '__file__':
            config_file_path = os.path.abspath(os.path.dirname(__file__))
        if config_file_path is not None:
            with open(config_file_path) as json_file:
                config_dict = json.load(json_file)
            super(Config, self).__init__(config_dict)
        elif kw != {}:
            super(Config, self).__init__(**kw)
        else:
            raise Exception('missing constructor arg - use file path or dict arg\'s')


def set_logger(config: dict):
    if config is None or config.get('LOG_DIR') is None:
        raise Exception('config missing config parameter "log_dir"')
    log_dir = config['LOG_DIR']
    log_level_config = config.get('LOG_LEVEL')
    log_levels = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
    log_level = log_levels.get(log_level_config)
    is_log_dir_created = False
    if log_level is None:
        raise Exception(
            f'Invalid LOG_LEVEL="{log_level_config}" in config_trans.json, use one of: ' + str(log_levels.keys()))
    if not os.path.isdir(log_dir):
        try:
            os.mkdir(log_dir)
        except Exception as exc:
            exc_trace = str(exc) + '\n\t' + traceback.format_exc()
            print(exc_trace)
        is_log_dir_created = True
    year_month = str(datetime.datetime.today())[:7]
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOG_LEVEL", log_level))
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s - %(funcName)s() - %(message)s")

    log_file_path = log_dir + "/translator-" + year_month + ".log"
    handler = logging.FileHandler(log_file_path, 'a', 'utf-8')
    handler.setFormatter(log_formatter)
    root.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root.addHandler(console_handler)
    if is_log_dir_created:
        log.info(f'Created log file: {log_file_path}/')
