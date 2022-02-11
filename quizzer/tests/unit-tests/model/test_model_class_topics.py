import json

from pytest import raises

from quz.model import Model
from quz.quiz import Quiz
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_wo_stored_files():
    m = Model(TMP_DIR)
    assert m.latest_quiz_topic == 'quiz'
    assert m.quiz_topics == ['quiz']


def test_with_stored_files():
    marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n'
    quiz = Quiz(marked_user_input=marked_user_input)
    data_dict = quiz.get_data_dict()

    with open(TMP_DIR + '/java-quiz.1.json', "w") as f:
        json.dump(data_dict, f)

    with open(TMP_DIR + '/sql-quiz.1.json', "w") as f:
        json.dump(data_dict, f)
    m = Model(TMP_DIR)
    assert m.latest_quiz_topic == 'java'
    assert m.quiz_topics == ['java', 'sql']


def test_with_saved_file_name():
    contents = {'LATEST_FILE_NAME': 'sql-tricks.1.json'}
    with open(TMP_DIR + '/latest_work.json', "w") as f:
        json.dump(contents, f)
    m = Model(TMP_DIR)
    assert m.latest_quiz_topic == 'sql'
    assert m.quiz_topics == ['java', 'sql']


def test_with_saved_file_name():
    contents = {'LATEST_FILE_NAME': 'basic-tricks.1.json'}
    with open(TMP_DIR + '/latest_work.json', "w") as f:
        json.dump(contents, f)
    with raises(AttributeError):
        Model(TMP_DIR)


def test_with_saved_file_name():
    quiz = Quiz(marked_user_input='?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n')
    with open(TMP_DIR + '/basic-quiz.2.json', "w") as f:
        json.dump(quiz.get_data_dict(), f)
    m = Model(TMP_DIR)
    assert m.latest_quiz_topic == 'basic'
    assert m.quiz_topics == ['basic', 'java', 'sql']
