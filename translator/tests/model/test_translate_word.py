import googletrans
import ltrans
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'DICTIONARY_DIR': TMP_DIR, 'LOG_LEVEL': 'INFO'}
ltrans.util.set_logger(CONFIG)

TRANSLATOR = googletrans.Translator()


def test_new_word():
    dictionary = english_french_dict()
    trans_word = ltrans.model.translate_word('funny', dictionary, TRANSLATOR)
    assert trans_word == 'drôle' or trans_word == 'marrant'


def test_existing_word():
    dictionary = english_french_dict()
    int_len = len(dictionary)
    trans_word = ltrans.model.translate_word('hello', dictionary, TRANSLATOR)
    assert trans_word == 'bonjour'
    assert len(dictionary) == int_len


def test_word_upper_case():
    dictionary = english_french_dict()
    int_len = len(dictionary)
    trans_word = ltrans.model.translate_word('Hello', dictionary, TRANSLATOR)
    assert trans_word == 'Bonjour'
    assert len(dictionary) == int_len


def test_word_w_delimiter():
    dictionary = french_english_dict()
    int_len = len(dictionary)
    trans_word = ltrans.model.translate_word("Aujourd'hui", dictionary, TRANSLATOR)
    assert trans_word == "Today"
    if len(dictionary) == int_len:
        print('words: ', dictionary.words())
    assert len(dictionary) == int_len


def french_english_dict():
    d = ltrans.model.Dictionary(CONFIG, 'French', 'English')
    d['Aujourd\'hui'] = 'Today'
    d['Bonjour'] = 'hello'
    return d


def english_french_dict():
    d = ltrans.model.Dictionary(CONFIG, 'English', 'French')
    d['Today'] = 'Aujourd\'hui'
    d['hello'] = 'bonjour'
    return d
