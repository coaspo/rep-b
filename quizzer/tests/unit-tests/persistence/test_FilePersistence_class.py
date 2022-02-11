import os

import pytest

import quz.model
import tests.t_util
from quz.persistence import FilePersistence

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
QUIZ_FILE_PFX = 'quiz'
CONFIG = {'LOG_DIR': TMP_DIR, 'QUIZZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}

quz.util.set_logger(CONFIG)


def _create_fake_domain_object(data_dict: dict) -> dict:
    return data_dict


def test_invalid_directories():
    FilePersistence('/non-dir/fake-dir')
    assert "JsonFileStorage failed" in FilePersistence.file_storage_err_msg


def test_obj_attrs():
    persistence = FilePersistence(TMP_DIR)
    assert persistence.file_storage_err_msg is None


def test_save():
    persistence = FilePersistence(TMP_DIR)

    quiz = {'fake..ques..': 'a'}
    persistence.save('quiz', quiz)
    assert persistence.status.endswith('quiz.1.json')

    quiz = {'fake2..ques..': 'a2'}
    persistence.save('quiz', quiz)
    assert persistence.status.endswith('quiz.2.json')


def test_get():
    persistence = FilePersistence(TMP_DIR)
    quiz = persistence.get(_create_fake_domain_object)
    assert 'quiz.2.json' in persistence.status
    assert '2/2  quiz.2' in persistence.description
    assert quiz == {'fake2..ques..': 'a2'}


def test_get_previous():
    persistence = FilePersistence(TMP_DIR)
    quiz = persistence.get_previous(_create_fake_domain_object)
    assert 'quiz.1.json' in persistence.status
    assert '1/2  quiz.1' in persistence.description
    assert quiz == {'fake..ques..': 'a'}
    quiz = persistence.get_previous(_create_fake_domain_object)
    assert 'quiz.1.json' in persistence.status
    assert '1/2  quiz.1' in persistence.description
    assert quiz == {'fake..ques..': 'a'}


def test_get_next():
    persistence = FilePersistence(TMP_DIR)
    quiz = persistence.get_next(_create_fake_domain_object)
    assert 'quiz.2.json' in persistence.status
    assert '2/2  quiz.2' in persistence.description
    assert quiz == {'fake2..ques..': 'a2'}
    quiz = persistence.get_next(_create_fake_domain_object)
    assert 'quiz.2.json' in persistence.status
    assert '2/2  quiz.2' in persistence.description
    assert quiz == {'fake2..ques..': 'a2'}


def test_update():
    persistence = FilePersistence(TMP_DIR)
    quiz_new = {'real?..ques..': 'A'}
    persistence.update(quiz_new)

    quiz = persistence.get(_create_fake_domain_object)
    assert 'quiz.2.json' in persistence.status
    assert '2/2  quiz.2' in persistence.description
    assert quiz == quiz_new


def test_delete():
    persistence = FilePersistence(TMP_DIR)
    quiz = persistence.get(_create_fake_domain_object)
    assert persistence.topics == ['quiz']
    assert quiz == {'real?..ques..': 'A'}
    assert len(os.listdir(TMP_DIR)) == 3

    persistence.delete()
    assert len(os.listdir(TMP_DIR)) == 2
    assert persistence.status.startswith('Deleted quiz file:')

    quiz = persistence.get(_create_fake_domain_object)
    assert persistence.status.startswith('Read quiz file:')
    assert quiz == {'fake..ques..': 'a'}
    with pytest.raises(Exception, match="Cannot delete last file."):
        persistence.delete()
