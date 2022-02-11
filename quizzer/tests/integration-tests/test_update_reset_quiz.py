import tkinter

from quz.controller import QuizController, QuizQuestionController
from quz.model import Model
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_update_marked_text():
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = QuizController(v, m)
    v.input_marked_text_area.insert('insert', '?What is 2+3\n'
                                              '-is 4\n'
                                              '+is 5\n\n'
                                              '=addition\n\n'
                                              '?1*2 = ?\n'
                                              '- = 1\n'
                                              '+ = 2\n'
                                              '- = 4\n\n')
    v.add_new_quiz_bt['state'] = tkinter.NORMAL
    c._add_new_quiz('fake-<Button-1>-event')
    assert v.status_label.cget('text').startswith('Saved quiz file')
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    assert 'What is 2+3' == v.question_label.cget('text')
    assert 'addition' == v.question_comment_label.cget('text')

    v.input_marked_text_area.delete('1.0', tkinter.END)
    marked_user_input = '?WHAT IS 100+100\n' \
                        '-300\n' \
                        '+200\n\n' \
                        '=BIG\n\n'
    v.input_marked_text_area.insert('insert', marked_user_input)
    m.reset_update_quiz(marked_user_input)
    c._populate_quiz_widgets()
    assert v.status_label.cget('text').startswith('Updated quiz file')
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    assert 'WHAT IS 100+100' == v.question_label.cget('text')
    assert 'BIG' == v.question_comment_label.cget('text')

    # prepare for next test:
    (is_selected, chk_bt) = v.answer_check_buttons[0]
    chk_bt.select()
    # following 2 statements are needed because of a tkinter defect ???
    is_selected = tkinter.IntVar(value=1)  # needed only when running all tests
    v.answer_check_buttons[1] = (is_selected, chk_bt)  # needed only when running all tests

    c2 = QuizQuestionController(v, m)
    c2._submit_question_answer('fake-mouse-click-event')


def test_reset_quiz():
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = QuizController(v, m)
    assert 'WHAT IS 100+100' == v.question_label.cget('text')
    (is_selected, chk_bt) = v.answer_check_buttons[1]
    assert is_selected.get() == 1
    marked_user_input = v.input_marked_text_area.get("1.0", tkinter.END).strip()
    m.reset_update_quiz(marked_user_input)
    c._populate_quiz_widgets()

    assert v.status_label.cget('text').startswith('Updated quiz file')
    (is_selected, chk_bt) = v.answer_check_buttons[1]
    assert is_selected.get() == 0


