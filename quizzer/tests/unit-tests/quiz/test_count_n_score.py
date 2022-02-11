from quz.quiz import Quiz
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_is_same_as():
    marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n- = 400\n+ = 2\n\n'
    quiz = Quiz(marked_user_input=marked_user_input)
    assert not quiz.is_any_question_answered()
    assert not quiz.are_all_questions_answered()
    quiz.set_selected_answer(1, True)
    assert quiz.is_any_question_answered()
    assert not quiz.are_all_questions_answered()
    assert str(
        quiz.current_question()) == 'QuizQuestion("What is 2+3", "addition", [MultipleChoiceAnswer' \
                                    '("is 4", False, False), MultipleChoiceAnswer("is 5", True, True)])'
    assert quiz.count_n_score() == '1/2'

    quiz.next_question()
    quiz.set_selected_answer(2, True)
    assert quiz.is_any_question_answered()
    assert quiz.are_all_questions_answered()
    assert quiz.count_n_score() == '2/2    score: 100% (2/2)'

    quiz.previous_question()
    quiz.set_selected_answer(0, True)
    assert quiz.count_n_score() == '1/2    score: 50% (1/2)'
