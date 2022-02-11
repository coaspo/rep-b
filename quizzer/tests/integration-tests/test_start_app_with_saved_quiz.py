import json
import tkinter

from quz.controller import QuizController
from quz.model import Model
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)

m: Model
v: View
c: View


def test_enter_marked_text():
    data_dict = {'current_question_index': 0, 'num_of_questions': 2,
                 'marked_user_input': '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n?1*2 = ?\n- = 1\n+ = 2\n- = 4',
                 'question1': 'What is 2+3', 'question1_answers': {'answer1': {'answer': 'is 4',
                                                                               'is_correct': False,
                                                                               'is_selected': False},
                                                                   'answer2': {'answer': 'is 5',
                                                                               'is_correct': True,
                                                                               'is_selected': False},
                                                                   'comment': 'addition',
                                                                   'num_of_answers': 2},
                 'question2': '1*2 = ?', 'question2_answers': {'answer1': {'answer': ' = 1',
                                                                           'is_correct': False,
                                                                           'is_selected': False},
                                                               'answer2': {'answer': ' = 2',
                                                                           'is_correct': True,
                                                                           'is_selected': False},
                                                               'answer3': {'answer': ' = 4',
                                                                           'is_correct': False,
                                                                           'is_selected': False},
                                                               'comment': None,
                                                               'num_of_answers': 3}}
    file_path = TMP_DIR + '/quiz.1.json'
    with open(file_path, "w", encoding='utf8') as f:
        json.dump(data_dict, f, ensure_ascii=False, sort_keys=False, indent=0)

    global m, v, c
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = QuizController(v, m)
    assert v.status_label.cget('text').startswith('Read quiz file')
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    assert 'What is 2+3' == v.question_label.cget('text')
    assert 'addition' == v.question_comment_label.cget('text')
    assert ('?What is 2+3\n'
            '-is 4\n'
            '+is 5\n\n'
            '=addition\n\n'
            '?1*2 = ?\n'
            '- = 1\n'
            '+ = 2\n'
            '- = 4\n') == v.input_marked_text_area.get("1.0", tkinter.END)


def test_answers():
    global m, v, c
    is_selected, chk_bt = v.answer_check_buttons[0]
    assert 0 == is_selected.get()
    assert 'is 4' == chk_bt.cget('text')
    is_selected.set(1)
    is_selected, chk_bt = v.answer_check_buttons[1]
    assert 0 == is_selected.get()
    assert 'is 5' == chk_bt.cget('text')

    is_selected, _ = v.answer_check_buttons[0]
    assert 1 == is_selected.get()
