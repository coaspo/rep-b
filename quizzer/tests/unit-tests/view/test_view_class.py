from quz.persistence import FilePersistence
from quz.quiz import Quiz
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_view_set_up():
    v = View('java', ['java', 'sql'], 'instructions....')
    marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n'
    quiz = Quiz(marked_user_input=marked_user_input)
    question = quiz.current_question()
    question.question

    #  v._root.update() # disabled because screen flashes

    # v.start()  # for manual testing

