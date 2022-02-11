import tkinter

from quz.controller import QuizController, QuizQuestionController
from quz.model import Model
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)

m: Model
v: View
c: QuizController


def test_next_quiz():
    global m, v, c
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = QuizController(v, m)
    c.bind_controls()
    c2 = QuizQuestionController(v, m)
    c2.bind_controls()
    v.input_marked_text_area.insert('insert', '?What is 2+3\n'
                                              '-is 4\n'
                                              '+is 5\n\n'
                                              '=addition\n\n'
                                              '?1*2 = ?\n'
                                              '- = 1\n'
                                              '- = 4\n'
                                              '+ = 2\n\n')
    v.add_new_quiz_bt['state'] = tkinter.NORMAL
    c._add_new_quiz('fake-<Button-1>-event')
    assert v.status_label.cget('text').startswith('Saved quiz file')
    assert v.question_count_n_score.cget('text') == '1/2'

    (is_selected, chk_bt) = v.answer_check_buttons[1]
    chk_bt.select()
    # following 2 statements are needed because of a tkinter defect ???
    is_selected = tkinter.IntVar(value=1)  # needed only when running all tests
    v.answer_check_buttons[1] = (is_selected, chk_bt)  # needed only when running all tests
    c2._submit_question_answer('fake-mouse-click-event')
    assert not m.quiz.are_all_questions_answered()
    assert v.question_count_n_score.cget('text') == '2/2'

    (is_selected, chk_bt) = v.answer_check_buttons[1]
    chk_bt.select()
    # following 2 statements are needed because of a tkinter defect ??>
    is_selected = tkinter.IntVar(value=1)  # needed only when running all tests
    v.answer_check_buttons[1] = (is_selected, chk_bt)  # needed only when running all tests
    c2._submit_question_answer('fake-mouse-click-event')
    assert m.quiz.are_all_questions_answered()
    assert not m.quiz.are_all_questions_answered_correctly()
    assert v.question_count_n_score.cget('text') == '2/2    score: 50% (1/2)'

    (is_selected, chk_bt) = v.answer_check_buttons[1]
    chk_bt.toggle()
    # following 2 statements are needed because of a tkinter defect ??>
    is_selected = tkinter.IntVar(value=0)  # needed only when running all tests
    v.answer_check_buttons[1] = (is_selected, chk_bt)  # needed only when running all tests
    (is_selected, chk_bt) = v.answer_check_buttons[2]
    chk_bt.select()
    # following 2 statements are needed because of a tkinter defect ??>
    is_selected = tkinter.IntVar(value=1)  # needed only when running all tests
    v.answer_check_buttons[2] = (is_selected, chk_bt)  # needed only when running all tests
    c2._submit_question_answer('fake-mouse-click-event')
    assert m.quiz.are_all_questions_answered()
    assert m.quiz.are_all_questions_answered_correctly()
    assert v.question_count_n_score.cget('text') == '2/2    score: 100% (2/2)'
