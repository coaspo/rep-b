import ltrans
import os
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'DICTIONARY_DIR': TMP_DIR, 'LOG_LEVEL': 'INFO'}
ltrans.util.set_logger(CONFIG)

def test_dict_file_path():
    dict_file_path = TMP_DIR +'/KlingonEnglish-dict.json'
    if os.path.isfile(dict_file_path):
        os.remove(dict_file_path)
    dicti = ltrans.model.Dictionary(CONFIG, 'Klingon', 'English')
    assert dicti._dict_file_path == dict_file_path
    assert len(dicti) == 0


def test_add_word():
    dicti = ltrans.model.Dictionary(CONFIG, 'Klingon', 'English')
    dicti['wa'] = 'one'
    assert dicti['wa'] == 'one'


def test_save():
    dicti = ltrans.model.Dictionary(CONFIG, 'Klingon', 'English')
    dicti['wa'] = 'one'
    dicti['cha'] = 'two'
    assert dicti.words() == {'wa': 'one', 'cha': 'two'}
    assert len(dicti) == 2
    dicti.save()

    dicti = ltrans.model.Dictionary(CONFIG,'Klingon', 'English')
    assert dicti._initial_len == 2
    assert len(dicti) == 2
    dicti['wa'] = 'one'
    dicti['cha'] = 'two'

