import logging
import os
import tkinter.font
import tkinter.scrolledtext
import tkinter.ttk
import webbrowser
from tkinter import DISABLED
from typing import List

log = logging.getLogger(__name__)


class View:
    @property
    def answer_check_buttons(self) -> list:
        return self._answer_check_buttons

    @property
    def clear_bt(self) -> tkinter.Button:
        return self._clear_bt

    @property
    def add_new_quiz_bt(self) -> tkinter.Button:
        return self._add_quiz_bt

    @property
    def next_quiz_bt(self) -> tkinter.Button:
        return self._next_quiz_bt

    @property
    def previous_quiz_bt(self) -> tkinter.Button:
        return self._previous_quiz_bt

    @property
    def previous_question_bt(self) -> tkinter.Button:
        return self._previous_question_bt

    @property
    def reset_update_quiz_bt(self) -> tkinter.Button:
        return self._reset_update_quiz_bt

    @property
    def delete_quiz_bt(self) -> tkinter.Button:
        return self._delete_quiz_bt

    @property
    def input_marked_text_area(self) -> tkinter.scrolledtext.ScrolledText:
        return self._input_marked_text_area

    @property
    def question_area(self):
        return self._question_area

    @property
    def next_question_bt(self) -> tkinter.Button:
        return self._next_question_bt

    @property
    def question_comment_label(self) -> tkinter.Label:
        return self._question_comment_label

    @property
    def question_label(self) -> tkinter.Label:
        return self._question_label

    @property
    def quiz_description_label(self):
        return self._quiz_description_label

    @property
    def quiz_topics(self) -> tkinter.ttk.Combobox:
        return self._quiz_topics

    @property
    def root(self) -> tkinter.Tk:
        return self._root

    @property
    def status_label(self) -> tkinter.Label:
        return self._status_label

    @property
    def submit_bt(self) -> tkinter.Button:
        return self._submit_bt

    @property
    def question_count_n_score(self) -> tkinter.Label:
        return self._question_count_n_score

    def __init__(self, latest_quiz_topic: str, quiz_topics: list, instructions: str):
        root = tkinter.Tk()
        root.title("Quiz maker/taker")
        self._answer_check_buttons: List[object, object] = []
        self._root = root

        self._init_menu(latest_quiz_topic, quiz_topics, root)
        self._init_scroll_frames(root)
        self._init_bottom_status_label(root, instructions)
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Finished creating view")

    def _init_menu(self, latest_quiz_topic: str, quiz_topics: list, root: tkinter.Tk):
        light_yellow = '#ffffcc'
        frame = tkinter.Frame(root, height=500)
        menu_background_color = light_yellow
        frame.configure(background=menu_background_color)
        frame.pack(fill=tkinter.BOTH, expand=False)

        self._init_topics_menu(latest_quiz_topic, quiz_topics, frame, menu_background_color)
        self._init_persistence_menu(frame, menu_background_color)

    def _init_topics_menu(self, latest_quiz_topic: str, quiz_topics: list, frame, frame_color):
        self._clear_bt = tkinter.Button(frame, text="  Clear  ")
        self._clear_bt.pack(side=tkinter.LEFT, padx=12, pady=2)
        topic_label = tkinter.Label(frame, text="   Quiz topic:", bg=frame_color)
        topic_label.pack(side=tkinter.LEFT, pady=2)

        self.variableCombo_value = tkinter.StringVar()
        self._quiz_topics = tkinter.ttk.Combobox(frame, width=10, height=12, font=("Arial", 9),
                                                 values=quiz_topics, textvariable=self.variableCombo_value)
        if len(quiz_topics) > 0 and latest_quiz_topic in quiz_topics:
            self._quiz_topics.current(quiz_topics.index(latest_quiz_topic))
        self._quiz_topics.pack(side=tkinter.LEFT, padx=5, pady=2)

        spacer_label = tkinter.Label(frame, text=None, bg=frame_color)
        spacer_label.pack(side=tkinter.LEFT, padx=10)

    def _init_persistence_menu(self, frame, frame_color):
        self._add_quiz_bt = tkinter.Button(frame, text=u'\u2795', height=1)
        self._add_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._reset_update_quiz_bt = tkinter.Button(frame, text=u'  \u2b6e  ', height=1)
        self._reset_update_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._delete_quiz_bt = tkinter.Button(frame, text=u'\u274C ')
        self._delete_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)

        self._previous_quiz_bt = tkinter.Button(frame, text=u'  \u2bc7  ', height=1)
        self._previous_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._next_quiz_bt = tkinter.Button(frame, text=u'  \u2bc8   ', height=1)
        self._next_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._quiz_description_label = tkinter.Label(frame, text="", anchor='w', bg=frame_color)
        self._quiz_description_label.config(width=50)
        self._quiz_description_label.pack(side=tkinter.LEFT, padx=2, pady=2)

        help_label = tkinter.Label(frame, text="Help", fg="blue", bg=frame_color, cursor="hand2")
        font = tkinter.font.Font(help_label, help_label.cget("font"))
        font.configure(underline=True)
        help_label.configure(font=font)
        help_label.pack(side=tkinter.LEFT, padx=50, pady=2)
        help_label.bind("<Button-1>", lambda e: webbrowser.get('windows-default').open(
            "file://" + os.path.realpath("./quz/help.html")))

    def _init_scroll_frames(self, root: tkinter.Tk):
        frame = tkinter.Frame(root)
        self._input_marked_text_area = tkinter.scrolledtext.ScrolledText(frame)
        self._input_marked_text_area.pack(side=tkinter.LEFT, pady=2, fill='both', expand=1)
        self._question_area = tkinter.Frame(frame, bg="white")

        self._init_question_frame()
        self._question_area.pack(side=tkinter.LEFT, pady=2, fill='both', expand=1)
        frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def _init_question_frame(self):
        self._question_label = tkinter.Label(self._question_area, fg="blue", bg='white', width=90, justify=tkinter.LEFT,
                                             anchor="w")
        self._question_label.grid(row=0, column=0, padx=10, pady=10, sticky=(tkinter.N, tkinter.S, tkinter.E))
        self._question_comment_label = tkinter.Label(self._question_area, fg="blue", bg='white', anchor=tkinter.W,
                                                     justify=tkinter.LEFT)
        self._question_comment_label.place(x=10, y=300, width=500, height=25)

        self._submit_bt = tkinter.Button(self._question_area, text="  Submit  ", state=tkinter.DISABLED)
        self._submit_bt.place(x=5, y=330, width=100, height=25)
        self._previous_question_bt = tkinter.Button(self._question_area, text=u' \u2bc7 ', height=1, state=DISABLED)
        self._previous_question_bt.place(x=160, y=330, width=40, height=25)
        self._next_question_bt = tkinter.Button(self._question_area, text=u' \u2bc8  ', height=1, state=DISABLED)
        self._next_question_bt.place(x=210, y=330, width=40, height=25)
        self._question_count_n_score = tkinter.Label(self._question_area, fg="blue", bg='white', width=150, text='aaaa')
        self._question_count_n_score.place(x=280, y=330, width=150, height=25)

    def _init_bottom_status_label(self, root, instructions: str):
        self._status_label = tkinter.Label(root, bg="#eeffee", fg='black')
        self._status_label['text'] = instructions
        self._status_label.pack(side=tkinter.LEFT, fill='both', expand='yes')

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

    def clear_screen(self):
        self.add_new_quiz_bt['state'] = tkinter.NORMAL
        self.set_buttons_state(tkinter.DISABLED)
        self.input_marked_text_area.delete('1.0', tkinter.END)
        self.input_marked_text_area.insert(tkinter.END, '')
        self.quiz_description_label['text'] = ''
        self.status_label['text'] = ''
        self.clear_quiz_question()

    def set_buttons_state(self, state):
        self.reset_update_quiz_bt['state'] = state
        self.delete_quiz_bt['state'] = state
        self.submit_bt['state'] = state
        self.next_question_bt['state'] = state
        self.previous_question_bt['state'] = state

    def clear_quiz_question(self):
        for (data, obj) in self.answer_check_buttons:
            if type(data) is tkinter.StringVar:
                obj[0].destroy()
                obj[1].destroy()
            elif type(data) is tkinter.IntVar:
                obj.destroy()
        self.answer_check_buttons.clear()
        self._question_label['text'] = ''
        self.question_comment_label['text'] = ''
        self.next_question_bt.configure(state=DISABLED)
        self.previous_question_bt.configure(state=DISABLED)
        self.submit_bt.configure(state=DISABLED)


def make_multiple_lines(line: str) -> str:
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


if __name__ == '__main__':
    v = View('quiz', ['java', 'sql'], 'This is a manual layout test. To run the application, run cli.py')
    print('start')
    v.start()
