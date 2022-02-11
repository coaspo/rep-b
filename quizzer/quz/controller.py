import json
import logging
import os
import tkinter
import tkinter.ttk
import traceback
from tkinter import messagebox

from quz.model import Model
from quz.quiz import QuizError
from quz.util import Config, set_logger
from quz.view import View

log = logging.getLogger(__name__)


class AbstractController:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model

    def handle_exception(self, msg: str, exc: Exception = None):
        if exc is None:
            log.error(msg)
            self._update_status(msg, True)
        else:
            msg_exc = msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            print(msg + '\n\t' + msg_trace)
            if type(exc) is not QuizError:
                log.error(msg + '\n\t' + msg_trace)
            self._update_status(msg_exc, True)

    def _update_status(self, text: str, is_err=False):
        self.view.status_label['text'] = text
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_label.config(bg=background)

    def _populate_quiz_widgets(self):
        if self.model.quiz is None:
            self.view.clear_screen()
        else:
            self.view.add_new_quiz_bt['state'] = tkinter.DISABLED
            self.view.set_buttons_state(tkinter.NORMAL)
            self.view.input_marked_text_area.delete('1.0', tkinter.END)
            self.view.input_marked_text_area.insert(tkinter.END, self.model.quiz.marked_user_input)
            self.view.quiz_description_label['text'] = self.model.quiz_description
            self._populate_question_widgets()
        self._update_status(self.model.status_msg)

    def _populate_question_widgets(self):
        question = self.model.quiz.current_question()
        self.view.question_label['text'] = AbstractController._make_multiple_lines(question.question)
        cmt = '' if question.comment is None else question.comment
        self.view.question_count_n_score['text'] = self.model.quiz.count_n_score()
        self.view.question_comment_label['text'] = cmt
        self._populate_answers_widgets()

    def _populate_answers_widgets(self):
        for (data, obj) in self.view.answer_check_buttons:
            if type(data) is tkinter.StringVar:
                obj[0].destroy()
                obj[1].destroy()
            elif type(data) is tkinter.IntVar:
                obj.destroy()
            else:
                raise Exception(f'unrecognized data type: {type(data)}')

        self.view.answer_check_buttons.clear()
        answers = self.model.quiz.current_question().answers
        for i, answer in enumerate(answers):
            if len(answers) > 1:
                self._populate_multiple_choice_answers(answer, i)
            else:
                self._populate_fill_in_answer(answer)

    def _populate_fill_in_answer(self, answer):
        bg = 'white'
        label_fg = 'white'  # makes correct answer invisible
        label_bg = 'white'
        if self.model.quiz.are_all_questions_answered():
            if answer.is_answered_correctly():
                bg = '#cfc'
            elif not answer.is_answered_correctly() and len(answer.answer) > 0:
                bg = '#fdd'
                label_fg = 'black'  # make correct answer visible
                label_bg = '#cfc'
        answer_txt = tkinter.StringVar()
        answer_txt.set(answer.answer)
        entry = tkinter.Entry(self.view.question_area, textvariable=answer_txt, bg=bg)
        entry.grid(row=1, column=0, sticky=tkinter.W, padx=10, pady=2)
        label = tkinter.Label(self.view.question_area, text=answer.correct_answer, bg=label_bg, fg=label_fg)
        label.grid(row=2, column=0, sticky=tkinter.W, padx=10, pady=2)
        self.view.answer_check_buttons.append((answer_txt, (entry, label)))

    def _populate_multiple_choice_answers(self, answer, i):
        is_set = 1 if answer.is_selected else 0
        is_selected = tkinter.IntVar(value=is_set)
        bg = 'white'
        if self.model.quiz.are_all_questions_answered():
            if answer.is_correct:
                bg = '#cfc'
            elif not answer.is_correct and answer.is_selected:
                bg = '#fdd'
        chk_bt = tkinter.Checkbutton(self.view.question_area,
                                     text=AbstractController._make_multiple_lines(answer.answer), bg=bg,
                                     variable=is_selected, padx=15)
        # chk_bt.setvar('is_selected', is_selected)
        chk_bt.grid(row=i + 1, column=0, sticky=tkinter.W, pady=2)
        self.view.answer_check_buttons.append((is_selected, chk_bt))

    @staticmethod
    def _make_multiple_lines(line: str) -> str:
        if len(line) < 5:
            return line
        paragraph = []
        is_new_line_added = False
        line_num = 1
        for i, c in enumerate(line):
            paragraph.append(c)
            if 75 * line_num < i < 90 * line_num and c == ' ':
                if not is_new_line_added:
                    line_num += 1
                    paragraph.append('\n')
                    is_new_line_added = True
            else:
                is_new_line_added = False
        return ''.join(paragraph)


class QuizController(AbstractController):

    def __init__(self, view: View, model: Model):
        AbstractController.__init__(self, view, model)
        quiz = self.model.get_quiz()
        if quiz is not None:
            self._populate_quiz_widgets()

    def _clear_entire_screen(self, _):
        self.view.clear_screen()
        self.model.remove_quiz()
        print(self.model.quiz)
        self._update_status(Config.APP_INSTRUCTIONS)

    def _indicate_possible_update(self, _):
        try:
            topic = self.view.quiz_topics.get().strip()
            if len(topic) == 0:
                raise QuizError('Topic drop down is empty')
            self._update_combo_box_topics(topic)
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
            if self.model.quiz is not None and self.model.quiz.marked_user_input != marked_user_input:
                if self.model.quiz.is_any_question_answered():
                    n_original = len(self.model.quiz.marked_user_input)
                    n_current = len(marked_user_input)
                    self._update_status(f"Original/current marked text are {n_original}/{n_current} characters long."
                                        "Click circle button to reset/update or wait for prompt on closing the APP.")
        except Exception as e:
            self._update_status(str(e), True)
            if str(e) != Config.MARKED_TEXT_ERR:
                self.handle_exception('Unexpected error: ', e)

    def _create_new_quiz(self, marked_user_input):
        self.model.create_new_quiz(marked_user_input)
        topic = self.view.quiz_topics.get().strip()
        self.model.save_new_quiz(topic)
        self._populate_quiz_widgets()

    def _update_combo_box_topics(self, topic):
        combo_values = self.view.quiz_topics['values']
        if topic not in combo_values:
            if isinstance(combo_values, str):
                if len(combo_values.strip()):
                    combo_values = topic
                else:
                    combo_values = (combo_values, topic)
            else:
                combo_values += (topic,)
            self.view.quiz_topics['values'] = combo_values

    def _on_close_window(self):
        if self.model.quiz is not None:
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
            n_original = len(self.model.quiz.marked_user_input)
            n_current = len(marked_user_input)
            if n_original != n_current:
                is_to_recreate = messagebox.askyesno(title="Quiz inconsistency",
                                                     message=f"Original/current marked text ia {n_original}/{n_current}"
                                                             "characters long.\n\n"
                                                             "Would you like to update the quiz with the new mark-up?\n"
                                                             "This ERASES any entered answers.",
                                                     default=messagebox.NO, parent=self.view.root)
                if is_to_recreate:
                    self.model.reset_update_quiz(marked_user_input)
        self.view.stop()

    def _reset_quiz_topic(self, _):
        topic = self.view.quiz_topics.get()
        self.model.reset_quiz_topic(topic)
        self._populate_quiz_widgets()

    def _next_quiz(self, _):
        try:
            self.model.set_to_next_quiz()
            self._populate_quiz_widgets()
        except Exception as e:
            self.handle_exception('Unexpected err', e)

    def _previous_quiz(self, _):
        try:
            self.model.set_to_previous_quiz()
            self._populate_quiz_widgets()
        except Exception as e:
            self.handle_exception('Unexpected err', e)

    def _add_new_quiz(self, _):
        if self.view.add_new_quiz_bt['state'] == tkinter.NORMAL:
            topic = self.view.quiz_topics.get().strip()
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
            try:
                self.model.create_new_quiz(marked_user_input)
                self.model.save_new_quiz(topic)
                self._populate_quiz_widgets()
            except QuizError as e:
                self.view.status_label['text'] = str(e) + '  ' + Config.APP_INSTRUCTIONS
        else:
            self._update_status("To add a quiz, clear 'Clear' and on left panel: " + Config.APP_INSTRUCTIONS, True)

    def _delete_quiz(self, _):
        if self.model.quiz is not None:
            self._update_status("", False)
            is_to_delete = messagebox.askokcancel(title="Verify quiz delete",
                                                  message=f"Delete quiz:\n  {self.model.quiz_description}",
                                                  default=messagebox.CANCEL, parent=self.view.root)
            if is_to_delete:
                try:
                    self.model.delete_quiz()
                    self._populate_quiz_widgets()
                except Exception as e:
                    self.handle_exception('Unexpected err', e)

    def _reset_update_quiz(self, _):
        if self.model.quiz is not None:
            self._update_status("", False)
            is_to_reset = messagebox.askokcancel(title="Verify quiz update/rest",
                                                 message=f"Quiz:\n  {self.model.quiz_description}\n\n"
                                                         "Reset will save a new quiz from the mark-up text.\n"
                                                         "Any answers are removed.",
                                                 default=messagebox.CANCEL, parent=self.view.root)
            if is_to_reset:
                try:
                    marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
                    self.model.reset_update_quiz(marked_user_input)
                    self._populate_quiz_widgets()
                except Exception as e:
                    self.handle_exception('Unexpected err', e)

    def bind_controls(self):
        self.view.clear_bt.bind("<Button-1>", self._clear_entire_screen)
        self.view.add_new_quiz_bt.bind("<Button-1>", self._add_new_quiz)
        self.view.reset_update_quiz_bt.bind("<Button-1>", self._reset_update_quiz)
        self.view.delete_quiz_bt.bind("<Button-1>", self._delete_quiz)
        self.view.input_marked_text_area.bind("<Leave>", self._indicate_possible_update)
        self.view.quiz_topics.bind("<<ComboboxSelected>>", self._reset_quiz_topic)
        self.view.root.protocol("WM_DELETE_WINDOW", self._on_close_window)
        self.view.next_quiz_bt.bind("<Button-1>", self._next_quiz)
        self.view.previous_quiz_bt.bind("<Button-1>", self._previous_quiz)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


class QuizQuestionController(AbstractController):

    def _next_question(self, _):
        if self.view.next_question_bt['state'] != 'disabled':
            try:
                self.model.quiz.next_question()
                self._populate_quiz_widgets()
            except Exception as e:
                super().handle_exception('Next question err', e)

    def _previous_question(self, _):
        if self.view.previous_question_bt['state'] != 'disabled':
            try:
                self.model.quiz.previous_question()
                self._populate_quiz_widgets()
            except Exception as e:
                self.handle_exception('Previous question err', e)

    def _submit_question_answer(self, _):
        if self.view.submit_bt['state'] != 'disabled':
            try:
                for i, (value, obj) in enumerate(self.view.answer_check_buttons):
                    # (value, obj)  is either (is_selected, chk_bt)  or  (answer_txt, (entry, label))
                    if type(obj) == tkinter.Checkbutton:
                        self.model.quiz.set_selected_answer(i, value.get())
                    else:
                        self.model.quiz.set_fill_in_answer(value.get())
                self.model.update_quiz()
                self.model.quiz.next_question()
                self._populate_quiz_widgets()
            except Exception as e:
                self.handle_exception('Previous question err', e)

    def bind_controls(self):
        self.view.next_question_bt.bind("<ButtonRelease-1>", self._next_question)
        self.view.previous_question_bt.bind("<Button-1>", self._previous_question)
        self.view.submit_bt.bind("<Button-1>", self._submit_question_answer)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


def main():
    try:
        with open(os.path.dirname(__file__) + "/config_quizzer.json") as f:
            config = json.load(f)
        set_logger(config)
        if log.isEnabledFor(logging.DEBUG):
            log.info(f'config: {config}')

        m = Model(config['QUIZZES_DIR'])

        v = View(m.latest_quiz_topic, m.quiz_topics, Config.APP_INSTRUCTIONS)

        c = QuizController(v, m)
        c.bind_controls()
        c2 = QuizQuestionController(v, m)
        c2.bind_controls()

        log.info('>>> Starting view')
        v.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        print(exc_trace)
        log.error(exc_trace)
