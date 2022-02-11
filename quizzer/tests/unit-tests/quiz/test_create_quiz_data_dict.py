import pprint

import pytest

from quz.quiz import Quiz


def test_create_quiz_data_dict():
    marked_user_input = '?What is 2+3\n' \
                        '-is 4\n' \
                        '+is 5\n\n' \
                        '=addition\n\n' \
 \
                        '?1*2 = ?\n' \
                        '- = 1\n' \
                        '+ = 2\n' \
                        '- = 4\n' \
 \
                        '?What is 12+13\n' \
                        '-is 24\n' \
                        '+is 25\n\n' \
                        '=big addition\n\n'

    data_dict = Quiz._create_quiz_data_dict(marked_user_input)
    expected_data_dict = {'current_question_index': 0,
                          'num_of_questions': 3,
                          'marked_user_input': marked_user_input,
                          'question1': 'What is 2+3',
                          'question1_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': 'is 4'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': 'is 5'},
                                                'comment': 'addition',
                                                'num_of_answers': 2},
                          'question2': '1*2 = ?',
                          'question2_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': ' = 1'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': ' = 2'},
                                                'answer3': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': ' = 4'},
                                                'num_of_answers': 3},
                          'question3': 'What is 12+13',
                          'question3_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': 'is 24'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': 'is 25'},
                                                'comment': 'big addition',
                                                'num_of_answers': 2}}

    data_dict_lines = pprint.pformat(data_dict).split('\n')
    expected_data_dict_lines = pprint.pformat(expected_data_dict).split('\n')

    for i, line in enumerate(data_dict_lines):
        if i > len(expected_data_dict_lines) - 1:
            raise Exception(
                f'Actual larger than expected.\nactual/expected:\n{data_dict_lines}{expected_data_dict_lines}')
        if line != expected_data_dict_lines[i]:
            pytest.fail(f'json lines #{i} not equal ' +
                        f'\nactual/expected lines:\n{line}\n{expected_data_dict_lines[i]}' +
                        f'\nactual/expected DICTs:\n{data_dict}\n{expected_data_dict}')


def test_create_quiz_data_dict_with_fill_in():
    marked_user_input = '?What is 2+3\n' \
                        '+five\n\n' \
                        '=addition fill in\n\n' \
 \
                        '?1*2 = ?\n' \
                        '- = 1\n' \
                        '+ = 2\n' \
                        '- = 4\n'
    data_dict = Quiz._create_quiz_data_dict(marked_user_input)
    expected_data_dict = {'current_question_index': 0,
                          'num_of_questions': 2,
                          'marked_user_input': marked_user_input,
                          'question1': 'What is 2+3',
                          'question1_answers': {'answer1': {'answer': '',
                                                            'correct_answer': 'five'},
                                                'comment': 'addition fill in',
                                                'num_of_answers': 1},
                          'question2': '1*2 = ?',
                          'question2_answers': {'answer1': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': ' = 1'},
                                                'answer2': {'is_correct': True,
                                                            'is_selected': False,
                                                            'answer': ' = 2'},
                                                'answer3': {'is_correct': False,
                                                            'is_selected': False,
                                                            'answer': ' = 4'},
                                                'num_of_answers': 3}}

    data_dict_lines = pprint.pformat(data_dict).split('\n')
    expected_data_dict_lines = pprint.pformat(expected_data_dict).split('\n')

    for i, line in enumerate(data_dict_lines):
        if i > len(expected_data_dict_lines) - 1:
            raise Exception(
                f'Actual larger than expected.\nactual/expected:\n{data_dict_lines}{expected_data_dict_lines}')
        assert line == expected_data_dict_lines[i]
