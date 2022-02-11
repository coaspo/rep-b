from quz.quiz import MultipleChoiceAnswer
from quz.quiz import QuizQuestion
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_correct_answers():
    a1 = MultipleChoiceAnswer('4', is_correct=True, is_selected=True)
    a2 = MultipleChoiceAnswer('3', False, False)
    answers = [a1, a2]
    question = QuizQuestion('What is 2+2?', 'test question', answers)
    assert question.are_answers_correct()
    a3 = MultipleChoiceAnswer('04', True, True)
    answers = [a1, a2, a3]
    question = QuizQuestion('What is 2+2?', 'test question', answers)
    assert question.are_answers_correct()
    assert question.is_answered()


def test_incorrect_answers():
    a1 = MultipleChoiceAnswer('4', is_correct=True, is_selected=True)
    a2 = MultipleChoiceAnswer('3', False, True)
    answers = [a1, a2]
    question = QuizQuestion('What is 2+2?', 'test question', answers)
    assert not question.are_answers_correct()
    a3 = MultipleChoiceAnswer('04', True, False)
    answers = [a1, a3]
    question = QuizQuestion('What is 2+2?', 'test question', answers)
    assert not question.are_answers_correct()
    assert question.is_answered()

    a4 = MultipleChoiceAnswer('04', True, False)
    a5 = MultipleChoiceAnswer('10', False, False)
    answers = [a4, a5]
    question = QuizQuestion('What is 2+2?', 'test question', answers)
    assert not question.are_answers_correct()
    assert not question.is_answered()
