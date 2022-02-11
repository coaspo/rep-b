from quz.quiz import Quiz
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_quiz_obj_to_data_dict():
    marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n'
    quiz = Quiz(marked_user_input=marked_user_input)
    data_dict = quiz.get_data_dict()

    expected_quiz_data_dict = {'current_question_index': 0,
                               'num_of_questions': 2,
                               'marked_user_input': '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' 
                                                    '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n',
                               'question1': 'What is 2+3',
                               'question1_answers': {
                                   'answer1': {'is_correct': False, 'is_selected': False, 'answer': 'is 4'},
                                   'answer2': {'is_correct': True, 'is_selected': False, 'answer': 'is 5'},
                                   'comment': 'addition',
                                   'num_of_answers': 2},
                               'question2': '1*2 = ?',
                               'question2_answers': {
                                   'answer1': {'is_correct': False, 'is_selected': False, 'answer': ' = 1'},
                                   'answer2': {'is_correct': True, 'is_selected': False, 'answer': ' = 2'},
                                   'answer3': {'is_correct': False, 'is_selected': False, 'answer': ' = 4'},
                                   'comment': None,
                                   'num_of_answers': 3}}
    assert data_dict == expected_quiz_data_dict
