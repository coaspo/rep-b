from quz.persistence import FilePersistence
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
    quiz.set_selected_answer(1, True)
    quiz.next_question()
    quiz.set_selected_answer(2, True)
    assert quiz.count_n_score() == '2/2    score: 100% (2/2)'
    persistence = FilePersistence(TMP_DIR)
    persistence.save('quiz', quiz.get_data_dict())

    persistence = FilePersistence(TMP_DIR)
    quiz: Quiz = persistence.get(lambda data_dict: Quiz(quiz_data_dict=data_dict))
    assert quiz.is_any_question_answered()
    assert quiz.are_all_questions_answered()
    assert quiz.count_n_score() == '2/2    score: 100% (2/2)'


def test_mixed_questions():
    marked_user_input = '?2+3=\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2=\n+2'
    quiz = Quiz(marked_user_input=marked_user_input)
    quiz.set_selected_answer(1, True)
    quiz.next_question()
    quiz.set_fill_in_answer('2')
    assert quiz.count_n_score() == '2/2    score: 100% (2/2)'
    persistence = FilePersistence(TMP_DIR)
    persistence.save('quiz', quiz.get_data_dict())
    persistence = FilePersistence(TMP_DIR)
    quiz: Quiz = persistence.get(lambda data_dict: Quiz(quiz_data_dict=data_dict))
    assert quiz.is_any_question_answered()
    assert quiz.are_all_questions_answered()
    assert quiz.count_n_score() == '2/2    score: 100% (2/2)'
