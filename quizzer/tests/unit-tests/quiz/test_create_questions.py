from quz.quiz import MultipleChoiceAnswer, Quiz, FillInAnswer
from quz.quiz import QuizQuestion
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_create_questions():
    question1_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': 'is 4'},
                         'answer2': {'is_correct': True, 'is_selected': False, 'answer': 'is 5'},
                         'comment': 'addition',
                         'num_of_answers': 2}
    question2_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': ' = 1'},
                         'answer2': {'is_correct': True, 'is_selected': False, 'answer': ' = 2'},
                         'answer3': {'is_correct': False, 'is_selected': False, 'answer': ' = 4'},
                         'num_of_answers': 3}
    quiz_data_dict = {'current_question_index': 0,
                      'num_of_questions': 2,
                      'marked_user_input': '?aaa/n+bbb/n-ccc...',
                      'question1': 'What is 2+3',
                      'question1_answers': question1_answers,
                      'question2': '1*2 = ?',
                      'question2_answers': question2_answers}

    questions = Quiz._create_questions(quiz_data_dict)
    assert len(questions) == 2

    expected = QuizQuestion("What is 2+3", "addition", [MultipleChoiceAnswer("is 4", False, False),
                                                        MultipleChoiceAnswer("is 5", True, False)])
    assert questions[0] == expected

    expected = QuizQuestion("1*2 = ?", None, [MultipleChoiceAnswer(" = 1", False, False),
                                              MultipleChoiceAnswer(" = 2", True, False),
                                              MultipleChoiceAnswer(" = 4", False, False)])
    assert questions[1] == expected


def test_create_fill_in_questions():
    question1_answer = {'answer1': {'correct_answer': '5', 'answer': ''},
                        'comment': 'addition',
                        'num_of_answers': 1}
    question2_answer = {'answer1': {'correct_answer': '2', 'answer': ''},
                        'num_of_answers': 1}
    quiz_data_dict = {'current_question_index': 0,
                      'num_of_questions': 2,
                      'marked_user_input': '?aaa/n+bbb/n-ccc...',
                      'question1': 'What is 2+3',
                      'question1_answers': question1_answer,
                      'question2': '1*2 = ?',
                      'question2_answers': question2_answer}

    questions = Quiz._create_questions(quiz_data_dict)
    assert len(questions) == 2

    expected = QuizQuestion("What is 2+3", "addition", [FillInAnswer("5", '')])
    assert questions[0] == expected

    expected = QuizQuestion("1*2 = ?", None, [FillInAnswer("2", '')])
    assert questions[1] == expected


def test_create_mixed_questions():
    question1_answer = {'answer1': {'correct_answer': '5', 'answer': ''},
                        'comment': 'addition',
                        'num_of_answers': 1}
    question2_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': ' = 1'},
                         'answer2': {'is_correct': True, 'is_selected': False, 'answer': ' = 2'},
                         'answer3': {'is_correct': False, 'is_selected': False, 'answer': ' = 4'},
                         'num_of_answers': 3}
    question3_answer = {'answer1': {'correct_answer': '5', 'answer': '5'},
                        'comment': 'addition',
                        'num_of_answers': 1}
    quiz_data_dict = {'current_question_index': 0,
                      'num_of_questions': 3,
                      'marked_user_input': '?aaa/n+bbb/n-ccc...',
                      'question1': 'What is 2+3',
                      'question1_answers': question1_answer,
                      'question2': '1*2 = ?',
                      'question2_answers': question2_answers,
                      'question3': '2+3=',
                      'question3_answers': question3_answer,
                      }

    questions = Quiz._create_questions(quiz_data_dict)
    assert len(questions) == 3

    expected = QuizQuestion("1*2 = ?", None, [MultipleChoiceAnswer(" = 1", False, False),
                                              MultipleChoiceAnswer(" = 2", True, False),
                                              MultipleChoiceAnswer(" = 4", False, False)])
    assert questions[1] == expected

    expected = QuizQuestion("2+3=", "addition", [FillInAnswer("5", '5')])
    assert questions[2] == expected
