import ltrans
import ltrans.model
import tests.t_util
from ltrans.persistence import FilePersistence

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'SAVED_TRANSLATIONS_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
TRANSLATION = {'dest_language': 'French',
               'is_add_src': 0,
               'is_add_transliteration': 1,
               'src_language': 'English',
               'text_lines': 'This is\na test',
               'translated_text': 'This is\nCette est\n\na test\nune tester'}

ltrans.util.set_logger(CONFIG)


def test_invalid_directories():
    config = {}
    FilePersistence(config)
    assert FilePersistence.file_storage_err_msg == \
           'FileStorage failed - config missing parameter "SAVED_TRANSLATIONS_DIR"'

    config = {'SAVED_TRANSLATIONS_DIR': '/non-dir/fake-dir'}
    FilePersistence(config)
    assert FilePersistence.file_storage_err_msg.find(
        "FileStorage failed - [WinError 3] The system cannot find the path specified") > -1

    config = {'SAVED_TRANSLATIONS_DIR': './xyz:\n'}
    persistence = FilePersistence(config)
    assert persistence.file_storage_err_msg.find(
        "FileStorage failed - [WinError 267] The directory name is invalid") > -1


def test_obj_attrs():
    persistence = FilePersistence(CONFIG)
    assert persistence.file_storage_err_msg is None


def test_save_translation():
    persistence = FilePersistence(CONFIG)

    user_input = ltrans.model.UserInput('This is', 'English', 'French', False, False)
    translated_text = 'Cette est'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.startswith('Saved translation in:') and msg.endswith('English-French.1.json')

    user_input = ltrans.model.UserInput('This is\na test', 'English', 'French', False, False)
    translated_text = 'Cette est\nune tester'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.endswith('English-French.2.json')

    user_input = ltrans.model.UserInput('This\ntest', 'English', 'French', 0, 1)
    translated_text = 'This\nCette\n\ntest\ntester'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.endswith('English-French.3.json')


def test_next_and_previous_translation():
    persistence = FilePersistence(CONFIG)
    translation_1 = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 0,
                     'src_language': 'English',
                     'text_lines': 'This is',
                     'translated_text': 'Cette est'}
    translation_2 = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 0,
                     'src_language': 'English',
                     'text_lines': 'This is\na test',
                     'translated_text': 'Cette est\nune tester'}
    translation_3 = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 1,
                     'src_language': 'English',
                     'text_lines': 'This\ntest',
                     'translated_text': 'This\nCette\n\ntest\ntester'}

    file_path, msg, trans = persistence.next_translation()
    assert 'English-French.3.json' in file_path
    assert_dictionaries_equal(trans, translation_3)

    file_path, msg, trans = persistence.previous_translation()
    assert  'English-French.2.json' in file_path
    assert_dictionaries_equal(trans, translation_2)

    file_path, msg, trans = persistence.previous_translation()
    assert  'English-French.1.json' in file_path
    assert_dictionaries_equal(trans, translation_1)

    file_path, msg, trans = persistence.previous_translation()
    assert  'English-French.1.json' in file_path
    assert_dictionaries_equal(trans, translation_1)

    # test next:
    file_path, msg, trans = persistence.next_translation()
    assert  'English-French.2.json' in file_path
    assert_dictionaries_equal(trans, translation_2)

    file_path, msg, trans = persistence.next_translation()
    assert  'English-French.3.json' in file_path
    assert_dictionaries_equal(trans, translation_3)

    file_path, msg, trans = persistence.next_translation()
    assert  'English-French.3.json' in file_path
    assert_dictionaries_equal(trans, translation_3)

    user_input = ltrans.model.UserInput('One', 'Italian', 'Dutch', 0, 1)
    translated_text = 'Cette 123'
    persistence.update_translation(user_input, translated_text)
    file_path, msg, trans2 = persistence.next_translation()
    assert 'English-French.3.json' in file_path
    assert trans2['translated_text'] == 'Cette 123'
    assert trans2['dest_language'] == 'Dutch'
    assert trans2['text_lines'] == 'One'


def test_delete_translation():
    persistence = FilePersistence(CONFIG)
    persistence.delete_translation()


def assert_dictionaries_equal(dict1: dict, dict2: dict):
    keys1 = dict1.keys()
    assert len(keys1) == len(dict2.keys())
    for key in keys1:
        assert dict2.get(key) is not None
        assert dict1[key] == dict2[key]
