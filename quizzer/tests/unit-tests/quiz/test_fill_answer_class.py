from quz.quiz import FillInAnswer
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_correct_answer():
    answer = FillInAnswer('2', ' 5 ')
    assert not answer.is_answered_correctly()
    answer.answer = ' 2 '
    assert answer.is_answered_correctly()


def test_incorrect_answer():
    answer = FillInAnswer(' 2', '  2')
    assert answer.is_answered_correctly()
    answer.answer = '3'
    assert not answer.is_answered_correctly()
