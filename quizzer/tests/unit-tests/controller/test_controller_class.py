from quz.controller import QuizController, QuizQuestionController
from quz.model import Model
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_controller_set_up():
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, '<UI intructions>')

    c = QuizController(v, m)
    c.bind_controls()
    c2 = QuizQuestionController(v, m)
    c2.bind_controls()
