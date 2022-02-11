from quz.quiz import MultipleChoiceAnswer
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_correct_answer():
    answer = MultipleChoiceAnswer('is 1+1=2?', True, False)
    assert not answer.is_answered_correctly()
    answer.is_selected = True
    assert answer.is_answered_correctly()


def test_incorrect_answer():
    answer = MultipleChoiceAnswer('is 1+1=0?', False, False)
    assert answer.is_answered_correctly()
    answer.is_selected = True
    assert not answer.is_answered_correctly()
