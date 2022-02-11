import ltrans
import tests.t_util
import pytest
from ltrans.persistence import FileStorage

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'SAVED_TRANSLATIONS_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
ltrans.util.set_logger(CONFIG)


def test_invalid_directories():
    config = {}
    with pytest.raises(Exception, match=r'config missing parameter "SAVED_TRANSLATIONS_DIR"'):
        FileStorage(config)

    config = {'SAVED_TRANSLATIONS_DIR': '/non-dir/fake-dir'}
    with pytest.raises(Exception, match=r".*\[WinError 3] The system cannot find the path specified: 'C:\\\\non-dir\\\\fake-dir'"):
        FileStorage(config)


def test_valid_config():
    try:
        FileStorage(CONFIG)
    except Exception as e:
        pytest.fail("Unexpected error: " + str(e))


def test_latest_file_num():
    storage = FileStorage(CONFIG)
    with open(storage._save_dir + '/Italian-English.3.json', 'w') as f:
        f.write('{"a":1}')
    with open(storage._save_dir + '/Spanish-English.1.json', 'w') as f:
        f.write('{"b":2}')
    storage = FileStorage(CONFIG)
    assert storage._latest_file_number == 3
    assert storage._file_paths_index == 1
    assert len(storage._files_paths) == 2


def test_save_file():
    storage = FileStorage(CONFIG)
    file_pfx = 'English-French'
    example_dict = {'text': 'Yes', 'translation': 'Oui'}
    msg = storage.save(example_dict, file_pfx)
    assert msg.endswith('English-French.4.json')
    assert storage._latest_file_number == 4
    assert storage._file_paths_index == 2
    assert len(storage._files_paths) == 3


def test_read_next_and_prev():
    storage = FileStorage(CONFIG)
    actual_dict =  {'text': 'Yes', 'translation': 'Oui'}
    json_doc1 = {'a': 1}
    json2 = {'b': 2}

    assert storage._file_paths_index == 2
    file_path, msg, trans = storage.read_next()
    assert trans == json2 and storage._file_paths_index == 2

    file_path, msg, trans = storage.read_prev()
    assert trans == json_doc1 and storage._file_paths_index == 1
    file_path, msg, trans = storage.read_prev()
    assert trans == actual_dict and storage._file_paths_index == 0
    file_path, msg, trans = storage.read_prev()
    assert trans == actual_dict and storage._file_paths_index == 0

    file_path, msg, trans = storage.read_next()
    assert trans == json_doc1 and storage._file_paths_index == 1
    file_path, msg, trans = storage.read_next()
    assert trans == json2 and storage._file_paths_index == 2
    file_path, msg, trans = storage.read_next()
    assert trans == json2 and storage._file_paths_index == 2
    trans['b'] = 123
    storage.update(trans)
    file_path, msg, trans = storage.read_next()
    assert trans == {'b': 123} and storage._file_paths_index == 2

