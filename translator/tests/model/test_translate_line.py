import ltrans
import os
import shutil
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'DICTIONARY_DIR': TMP_DIR, 'LOG_LEVEL': 'INFO'}
ltrans.util.set_logger(CONFIG)


def test_no_new_words():
    dictionary = english_french_dict()
    int_len = len(dictionary)

    trans_line = ltrans.model.translate_line('Today is a fine day.', dictionary,  None)
    assert trans_line == "Aujourd'hui est une bien journée."
    assert len(dictionary) == int_len


def test_w_non_ltrs():
    dictionary = english_french_dict()
    int_len = len(dictionary)

    trans_line = ltrans.model.translate_line('Today, $10 is; a **fine** day.!?', dictionary, None)
    assert trans_line == "Aujourd'hui, $10 est; une **bien** journée.!?"
    assert len(dictionary) == int_len


def english_french_dict():
    english_french_dict2 = ltrans.model.Dictionary(CONFIG, 'English', 'French')
    english_french_dict2['Today'] = 'Aujourd\'hui'
    english_french_dict2['is'] = 'est'
    english_french_dict2['a'] = 'une'
    english_french_dict2['fine'] = 'bien'
    english_french_dict2['day'] = 'journée'
    assert len(english_french_dict2) == 5
    return english_french_dict2;
