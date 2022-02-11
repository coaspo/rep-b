import datetime
import logging
import ltrans.util
import shutil
import re
import os
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)


def test_set_logger():

    config = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'DEBUG'}
    ltrans.util.set_logger(config)
    log = logging.getLogger(__name__)
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'config={config}')

    ts = str(datetime.datetime.now())[:14]
    log.info(f'This is a test {ts}')

    files = os.listdir(TMP_DIR)
    log_file = [f for f in files if f.endswith('.log')][0]
    with open(config['LOG_DIR'] + '/'+ log_file) as f:
        file_txt = f.read()
    assert ts in file_txt
    assert 'test_set_logger() - This is a test' in file_txt

def test_config_wo_file():
    config = ltrans.util.Config(a=123, b='abc')
    assert config['a'] == 123
    assert config['b'] == 'abc'


def test_config_file():
    config_txt = '''
{
"TOP_OF_LIST_LANGUAGES": "Klingon,Spanish",
"DICTIONARY_DIR": "my-dict-dir"
}'''
    test_file_path = TMP_DIR + '/config2.json'
    with open(test_file_path, 'w') as f:
        f.write(config_txt)
    config = ltrans.util.Config(test_file_path)
    assert config['TOP_OF_LIST_LANGUAGES'] == 'Klingon,Spanish'
    assert config['DICTIONARY_DIR'] == 'my-dict-dir'


def test_non_ltrs_regex():
    actual = re.sub(ltrans.util.NON_LETTERS_REGEX, '', 'ab cd')
    assert actual == 'ab cd'
    actual = re.sub(ltrans.util.NON_LETTERS_REGEX, '', 'ab' + r'[\^$.|?*+()' + ' cd')
    assert actual == 'ab cd'
    actual = re.sub(ltrans.util.NON_LETTERS_REGEX, '', 'ab ,!@#$%&-_=:;"?<>/{}]] cd')
    assert actual == 'ab  cd'
