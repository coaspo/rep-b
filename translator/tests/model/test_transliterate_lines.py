import ltrans
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'DICTIONARY_DIR': TMP_DIR, 'LOG_LEVEL': 'INFO'}
ltrans.util.set_logger(CONFIG)


def test_tranliteration():
    lines = ['Αυτό είναι ένα τεστ', 'Μεταφράστε και μεταγράψτε λέξεις']
    transliterated_lines = ltrans.model.transliterate_lines(lines, 'Greek')
    assert transliterated_lines[0] == 'Auto einai ena test'
    assert transliterated_lines[1] == 'Metafraste kai metagrapste lexeis'


def test_tranliteration_one_line():
    lines = ['шоколад']
    transliterated_lines = ltrans.model.transliterate_lines(lines, 'Russian')
    assert transliterated_lines[0] == 'shokolad'


def test_non_tranliteration():
    lines = ['Good', 'Morning']
    transliterated_lines = ltrans.model.transliterate_lines(lines, 'English')
    assert transliterated_lines == []

