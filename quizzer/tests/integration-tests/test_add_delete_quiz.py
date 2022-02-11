import tkinter

import pytest

from quz.controller import QuizController
from quz.model import Model
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_add_quiz():
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
    v.input_marked_text_area.insert('insert', '?What is 10+10\n'
                                              '-30\n'
                                              '+20\n\n'
                                              '=big addition\n\n')
    v.add_new_quiz_bt['state'] = tkinter.NORMAL
    c._add_new_quiz('fake-<Button-1>-event')
    assert v.status_label.cget('text').startswith('Saved quiz file')
    assert v.quiz_description_label.cget('text').startswith('2/2  quiz.2.json')
    assert 'What is 10+10' == v.question_label.cget('text')
    assert 'big addition' == v.question_comment_label.cget('text')


def test_delete_quiz():
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = QuizController(v, m)
    assert v.status_label.cget('text').startswith('Read quiz file')
    assert v.quiz_description_label.cget('text').startswith('2/2  quiz.2.json')
    assert 'What is 10+10' == v.question_label.cget('text')
    assert 'big addition' == v.question_comment_label.cget('text')

    c.model.delete_quiz()
    c._populate_quiz_widgets()
    assert v.status_label.cget('text').startswith('Deleted quiz file')
    assert v.status_label.cget('text').find('Read quiz file') > -1
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    assert 'What is 2+3' == v.question_label.cget('text')
    assert 'addition' == v.question_comment_label.cget('text')

    with pytest.raises(Exception, match="Cannot delete last file."):
        c.model.delete_quiz()
