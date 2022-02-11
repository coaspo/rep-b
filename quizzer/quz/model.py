import logging
from typing import List

from quz.persistence import FilePersistence
from quz.quiz import Quiz

log = logging.getLogger(__name__)


def _create_quiz_object(data_dict: dict) -> Quiz:
    return Quiz(quiz_data_dict=data_dict)


class Model:
    def __init__(self, quiz_dir: str):
        self._status = None
        self._persistence = FilePersistence(quiz_dir)
        self._quiz: Quiz = self._persistence.get(_create_quiz_object)

    @property
    def latest_quiz_topic(self) -> str:
        return self._persistence.latest_topic

    @property
    def quiz(self) -> Quiz:
        return self._quiz

    @property
    def quiz_description(self) -> str:
        return self._persistence.description

    @property
    def quiz_topics(self) -> List[str]:
        return self._persistence.topics

    @property
    def status_msg(self) -> str:
        return self._status

    def remove_quiz(self):
        self._quiz = None

    def create_new_quiz(self, marked_user_input: str):
        self._quiz = Quiz(marked_user_input=marked_user_input)
        self._status = self._persistence.status

    def set_to_next_quiz(self):
        self._quiz = self._persistence.get_next(_create_quiz_object)
        self._status = self._persistence.status

    def set_to_previous_quiz(self):
        self._quiz = self._persistence.get_previous(_create_quiz_object)
        self._status = self._persistence.status

    def get_quiz(self) -> Quiz or dict:
        self._quiz = self._persistence.get(_create_quiz_object)
        self._status = self._persistence.status
        return self._quiz

    def reset_quiz_topic(self, quiz_topic: str):
        self._persistence.reset(quiz_topic)
        self._quiz = self._persistence.get_previous(_create_quiz_object)
        self._status = self._persistence.status

    def save_new_quiz(self, quiz_topic: str):
        self._persistence.save(quiz_topic, self._quiz.get_data_dict())
        self._status = self._persistence.status

    def delete_quiz(self):
        self._persistence.delete()
        delete_status = self._persistence.status
        self.get_quiz()
        self._status = delete_status + '  ' + self._status

    def reset_update_quiz(self, marked_user_input: str = None):
        self._quiz = Quiz(marked_user_input=marked_user_input)
        self.update_quiz()

    def update_quiz(self):
        self._persistence.update(self._quiz.get_data_dict())
        self._status = self._persistence.status

