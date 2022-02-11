import abc
import logging
from typing import List

import quz
from quz.util import Config


class QuizError(Exception):
    pass


class AbstractAnswer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_answered_correctly(self) -> bool:
        pass


class MultipleChoiceAnswer(AbstractAnswer):
    def __init__(self, answer: str, is_correct: bool, is_selected: bool):
        self._answer = answer
        self._is_correct = is_correct
        self._is_selected = is_selected
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(self.__repr__())

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def is_correct(self) -> bool:
        return self._is_correct

    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        self._is_selected = value

    def is_answered_correctly(self):
        return (self._is_selected and self._is_correct) or \
               (not self._is_selected and not self._is_correct)

    def __eq__(self, other) -> bool:
        if isinstance(other, MultipleChoiceAnswer):
            return self.answer == other.answer and \
                   self.is_correct == other.is_correct and \
                   self.is_selected == other.is_selected
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f'MultipleChoiceAnswer("{self.answer}", {self.is_correct}, {self.is_selected})'


class FillInAnswer(AbstractAnswer):
    def __init__(self, correct_answer: str, answer: str):
        self._answer = answer.strip()
        self._correct_answer = correct_answer.strip()
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(self.__repr__())

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def correct_answer(self) -> str:
        return self._correct_answer

    @answer.setter
    def answer(self, value: bool) -> None:
        self._answer = value.strip()

    def is_answered_correctly(self):
        if self._answer is None:
            return False
        answer = self._answer.replace(' ', '')
        correct_answer = self._correct_answer.replace(' ', '')
        return answer == correct_answer

    def __eq__(self, other) -> bool:
        if isinstance(other, FillInAnswer):
            return self.answer == other.answer and \
                   self.correct_answer == other.correct_answer
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f'FillInAnswer("{self.correct_answer}", "{self.answer}")'


class QuizQuestion:
    def __init__(self, question: str, comment: str or None, answers: List[AbstractAnswer]):
        self._question = question
        self._comment = comment
        self._answers = answers
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(self.__repr__())

    @property
    def question(self) -> str:
        return self._question

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def answers(self) -> List[AbstractAnswer]:
        return self._answers

    def are_answers_correct(self) -> bool:
        for answer in self._answers:
            if not answer.is_answered_correctly():
                return False
        return True

    def is_answered(self) -> bool:
        for answer in self._answers:
            if answer.is_selected:
                return True
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, QuizQuestion):
            return self.question == other.question and \
                   self.comment == other.comment and \
                   self.answers == other.answers
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        comment = self.comment
        if comment is not None:
            comment = '"' + comment + '"'
        return f'QuizQuestion("{self.question}", {comment}, {self.answers})'


class Quiz:
    """ marked_user_input when quiz is created from GUI, quiz_data_dict when quiz is created from persistence"""

    def __init__(self, marked_user_input: str = None, quiz_data_dict: dict = None):
        log = logging.getLogger(__name__)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                f' marked_user_input={marked_user_input}\nquiz_data_dict={quiz_data_dict}')
        if quiz_data_dict is None and marked_user_input is None:
            raise ValueError(f'marked_user_input and quiz_data_dict are both none')
        elif quiz_data_dict is not None and marked_user_input is not None:
            raise ValueError(f'marked_user_input or quiz_data_dict must be none')
        if quiz_data_dict is None:
            self._quiz_data_dict = Quiz._create_quiz_data_dict(marked_user_input)
        else:
            self._quiz_data_dict = quiz_data_dict
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'quiz_data_dict={self._quiz_data_dict}')
        self._quiz_questions: List[QuizQuestion] = Quiz._create_questions(self._quiz_data_dict)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'questions={self.questions}')

        self._current_question_index = self._quiz_data_dict['current_question_index']
        self._marked_user_input: str = self._quiz_data_dict['marked_user_input']
        self._num_of_questions = self._quiz_data_dict['num_of_questions']
        self._are_questions_answered: List[bool] = self._find_questions_answered()
        self._are_questions_answered_correctly: List[bool] = self._find_questions_answered_correctly()

    def _find_questions_answered(self) -> List[bool]:
        is_question_answered = self._num_of_questions * [False]
        for i, question in enumerate(self._quiz_questions):
            answers = question.answers
            for answer in answers:
                if len(answers) > 1 and answer.is_selected:
                    is_question_answered[i] = True
                    break
                elif len(answers) == 1 and len(answer.answer) > 0:
                    is_question_answered[i] = True
        return is_question_answered

    def _find_questions_answered_correctly(self) -> List[bool]:
        are_questions_answered_correctly = []
        for question in self._quiz_questions:
            are_questions_answered_correctly.append(question.are_answers_correct())
        return are_questions_answered_correctly

    @property
    def num_of_questions(self) -> int:
        return self._num_of_questions

    @property
    def marked_user_input(self) -> str:
        return self._marked_user_input

    @property
    def questions(self) -> List[QuizQuestion]:
        return self._quiz_questions

    @property
    def current_question_index(self) -> int:
        return self._current_question_index

    def next_question(self) -> QuizQuestion:
        if not self.are_all_questions_answered() or self.are_all_questions_answered_correctly():
            if self._current_question_index < len(self._quiz_questions) - 1:
                self._current_question_index += 1
        else:
            i = self._current_question_index
            while True:
                if i < len(self._quiz_questions) - 1:
                    i += 1
                else:
                    break
                if not self._are_questions_answered_correctly[i]:
                    self._current_question_index = i
                    break
        return self.current_question()

    def current_question(self) -> QuizQuestion:
        return self._quiz_questions[self._current_question_index]

    def previous_question(self) -> QuizQuestion:
        if not self.are_all_questions_answered() or self.are_all_questions_answered_correctly():
            if self._current_question_index > 0:
                self._current_question_index -= 1
        else:
            i = self._current_question_index
            while True:
                if i > 0:
                    i -= 1
                else:
                    break
                if not self._are_questions_answered_correctly[i]:
                    self._current_question_index = i
                    break
        return self.current_question()

    def set_selected_answer(self, answer_index: int, is_selected: bool) -> None:
        answers = self.current_question().answers
        if type(answers[answer_index]) is not quz.quiz.MultipleChoiceAnswer:
            raise QuizError('invalid type in: ' + answers[answer_index])

        answers[answer_index].is_selected = is_selected
        is_answered = False
        for answer in answers:
            if answer.is_selected:
                is_answered = True
                break
        self._are_questions_answered_correctly[
            self._current_question_index] = self.current_question().are_answers_correct()
        self._are_questions_answered[self._current_question_index] = is_answered

    def set_fill_in_answer(self, answer: str) -> None:
        if len(answer.strip()) == 0:
            return
        answers = self.current_question().answers
        if len(answers) > 1:
            raise QuizError('invalid type in answers=' + answers)
        answers[0].answer = answer
        self._are_questions_answered_correctly[self._current_question_index] = answer == answers[0].correct_answer
        self._are_questions_answered[self._current_question_index] = True

    def is_any_question_answered(self) -> bool:
        return max(self._are_questions_answered)

    def are_all_questions_answered(self) -> bool:
        return min(self._are_questions_answered)

    def are_all_questions_answered_correctly(self) -> bool:
        return min(self._are_questions_answered_correctly)

    def count_n_score(self) -> str:
        count = f'{self.current_question_index + 1}/{len(self._quiz_questions)}'
        if self.are_all_questions_answered():
            ratio, percent = self._score()
            score = f'    score: {percent} ({ratio})'
        else:
            score = ''
        return f'{count}{score}'

    def _score(self) -> tuple:
        num_of_correct_questions = 0
        num_of_questions = len(self._quiz_questions)
        for question in self._quiz_questions:
            if question.are_answers_correct():
                num_of_correct_questions += 1
        ratio = f'{num_of_correct_questions}/{num_of_questions}'
        percent = round(100. * num_of_correct_questions / num_of_questions)
        return ratio, f'{percent}%'

    def get_data_dict(self) -> dict:
        data_dict = {'current_question_index': self.current_question_index,
                     'num_of_questions': self.num_of_questions,
                     'marked_user_input': self.marked_user_input}
        for i in range(self.num_of_questions):
            quiz_question: QuizQuestion = self.questions[i]
            key_i = 'question' + str(i + 1)
            data_dict[key_i] = quiz_question.question
            question_answers_dict = dict()
            for j in range(len(quiz_question.answers)):
                answer = quiz_question.answers[j]
                if type(answer) == MultipleChoiceAnswer:
                    answer_dict = {'answer': answer.answer, 'is_correct': answer.is_correct,
                                   'is_selected': answer.is_selected}
                else:
                    answer_dict = {'correct_answer': answer.correct_answer, 'answer': answer.answer}
                key_j = 'answer' + str(j + 1)
                question_answers_dict[key_j] = answer_dict
            question_answers_dict['comment'] = quiz_question.comment
            question_answers_dict['num_of_answers'] = len(quiz_question.answers)
            key = key_i + '_answers'
            data_dict[key] = question_answers_dict
        return data_dict

    def __repr__(self) -> str:
        return f'Quiz(current_question_index={self._current_question_index}, num_of_questions=' \
               f'{self.num_of_questions}, {self._quiz_questions})'

    def is_same_as(self, other) -> bool:
        if isinstance(other, Quiz):
            if self.num_of_questions != other.num_of_questions:
                return False
            for i, question in enumerate(self.questions):
                if question.question != other.questions[i].question or \
                        question.comment != other.questions[i].comment or \
                        len(question.answers) != len(other.questions[i].answers):
                    return False
                other_answers = other.questions[i].answers
                for j, answer in enumerate(question.answers):
                    if answer.answer != other_answers[j].answer or \
                            answer.is_correct != other_answers[j].is_correct:
                        return False
            return True
        return False

    @staticmethod
    def _create_quiz_data_dict(marked_user_input: str) -> dict:
        text_lines = marked_user_input.strip().split('\n')
        if len(text_lines) < 2:
            raise QuizError(Config.MARKED_TEXT_ERR)
        quiz_data_dict = {'current_question_index': 0, 'marked_user_input': marked_user_input}
        num_of_answers = 0
        num_of_questions = 0
        question_answers = {}
        question_text = None
        comment = None

        for i, line in enumerate(text_lines):
            line = line.strip()
            next_line = None if i == len(text_lines) - 1 else text_lines[i + 1]
            is_next_line_an_answer = False
            if next_line is not None and (next_line.startswith('+') or next_line.startswith('-')):
                is_next_line_an_answer = True
            if len(line) == 0:
                continue

            if line.startswith('?'):
                if num_of_questions != 0:
                    Quiz._add_question_to_quiz_data_dict(comment, num_of_answers, num_of_questions, question_answers,
                                                         question_text, quiz_data_dict)
                question_text = line[1:]
                num_of_questions += 1

                num_of_answers = 0
                question_answers = {}
                comment = None
            elif line.startswith('+') or line.startswith('-'):
                num_of_answers += 1
                pass
                if num_of_answers == 1 and not is_next_line_an_answer:
                    answer = {'answer': '', 'correct_answer': line[1:]}
                else:
                    answer = {'is_correct': line.startswith('+'), 'is_selected': False, 'answer': line[1:]}
                pass
                question_answers['answer' + str(num_of_answers)] = answer
            elif line.startswith('='):
                if comment is not None:
                    raise QuizError(f'More than one comment for question;  line#{i}; line={line}')
                comment = line[1:]
            elif line.startswith('/'):
                pass
            else:
                raise QuizError(f'First character is not: ?+-=/  line#{i}; line={line}')

        Quiz._add_question_to_quiz_data_dict(comment, num_of_answers, num_of_questions, question_answers, question_text,
                                             quiz_data_dict)
        quiz_data_dict['num_of_questions'] = num_of_questions
        return quiz_data_dict

    @staticmethod
    def _add_question_to_quiz_data_dict(comment: str, num_of_answers: int, num_of_questions: int,
                                        question_answers: dict,
                                        question_text: str, quiz_data_dict: dict):
        question_answers['num_of_answers'] = num_of_answers
        if comment is not None:
            question_answers['comment'] = comment
        quiz_data_dict['question' + str(num_of_questions)] = question_text
        quiz_data_dict['question' + str(num_of_questions) + '_answers'] = question_answers

    @staticmethod
    def _create_questions(_quiz_data_dict: dict) -> List[QuizQuestion]:
        num_of_questions = _quiz_data_dict['num_of_questions']
        questions = []
        for i in range(1, num_of_questions + 1):
            key = 'question' + str(i)
            question_text = _quiz_data_dict[key]
            key2 = key + '_answers'
            answers_dict = _quiz_data_dict[key2]
            comment = answers_dict.get('comment')
            answers = Quiz._create_answers(answers_dict)
            quiz_question = QuizQuestion(question_text, comment, answers)
            questions.append(quiz_question)
        return questions

    @staticmethod
    def _create_answers(answers_dict: dict) -> List[AbstractAnswer]:
        num_of_answers = answers_dict['num_of_answers']
        answers = []
        for j in range(1, num_of_answers + 1):
            key = 'answer' + str(j)
            answer_dict = answers_dict[key]
            if num_of_answers > 1:
                text = answer_dict['answer']
                is_correct = answer_dict['is_correct']
                is_selected = answer_dict['is_selected']
                answer = MultipleChoiceAnswer(text, is_correct, is_selected)
            else:
                text = answer_dict['correct_answer']
                text_typed = answer_dict['answer']
                answer = FillInAnswer(text, text_typed)
            answers.append(answer)
        return answers
