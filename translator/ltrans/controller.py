from ltrans.model import Model
from ltrans.persistence import FilePersistence
from ltrans.reference import LANGUAGE_NAMES_ABBR
from ltrans.reference import TRANSLITERATE_LANGUAGE_NAMES
from ltrans.userinput import UserInput
from ltrans.userinput import UserInputError
from ltrans.util import Config
from ltrans.util import set_logger
from ltrans.view import View
import googletrans
import json
import logging
import os
import tkinter
import tkinter.ttk
import traceback

log = logging.getLogger(__name__)


class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model
        self.delete_bt_click_count = 0

    def get_user_input(self) -> UserInput:
        text = self.view.input_frame.get("1.0", tkinter.END)
        if text.strip() == '':
            raise UserInputError('Source text not entered')
        src_language = self.view.src_language.get()
        destination_language = self.view.destination_language.get()
        is_add_source = self.view.is_add_src.get()
        is_add_transliteration = self.view.is_add_transliteration.get()
        return UserInput(text, src_language, destination_language, is_add_source, is_add_transliteration)

    def update_status(self, text: str, is_err=False):
        self.view.status_label['text'] = text
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_label.config(bg=background)

    def clear_screen(self, _):
        self.delete_bt_click_count = 0
        self.view.src_language.set(self.view.language_names[0])
        self.view.destination_language.set(self.view.language_names[1])
        self.view.add_source_check_bt.deselect()
        self.view.add_transliteration_check_bt.config(state=tkinter.DISABLED)
        self.update_status(Config.TRANSLATE_INSTRUCTIONS)
        self.view.delete_bt.config(state=tkinter.DISABLED)
        self.view.update_bt.config(state=tkinter.DISABLED)
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        self.view.persistence_status['text'] = ''

    def handle_exception(self, msg: str, exc=None):
        if exc is None:
            log.error(msg)
            self.update_status(msg, True)
        else:
            msg_exc = msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            if type(exc) is not UserInputError:
                log.error(msg + '\n\t' + msg_trace)
            self.update_status(msg_exc, True)

    @staticmethod
    def set_check_button(button: tkinter.Checkbutton, value: int):
        if value == 1:
            button.select()
        else:
            button.deselect()


class TranslationController(Controller):
    def _swap_languages(self, _):
        src_language = self.view.src_language.get()
        destination_language = self.view.destination_language.get()

        for index, lang_name in enumerate(self.view.language_names):
            if lang_name == src_language:
                self.view.destination_language.current(index)
                break

        for index, lang_name in enumerate(self.view.language_names):
            if lang_name == destination_language:
                self.view.src_language.current(index)
                break

        src_text = self.view.input_frame.get("1.0", tkinter.END).strip()
        dest_text = self.view.output_frame.get("1.0", tkinter.END).strip()
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        self.view.input_frame.insert(tkinter.INSERT, dest_text)
        self.view.output_frame.insert(tkinter.INSERT, src_text)

    def _update_transliteration(self, _):
        try:
            src_language = self.view.src_language.get()
            destination_language = self.view.destination_language.get()
            if src_language in TRANSLITERATE_LANGUAGE_NAMES or destination_language in TRANSLITERATE_LANGUAGE_NAMES:
                self.view.add_transliteration_check_bt.configure(state=tkinter.NORMAL)
            else:
                self.view.add_transliteration_check_bt.configure(state=tkinter.DISABLED)
                Controller.set_check_button(self.view.add_transliteration_check_bt, 0)
        except Exception as e:
            self.handle_exception('', e)

    def _translate_text(self, _):
        try:
            user_input = super().get_user_input()
            self.view.output_frame.delete('1.0', tkinter.END)
            trans_text = self.model.translate(user_input)
            self.view.output_frame.insert(tkinter.END, trans_text)
            super().update_status(Config.SAVE_INSTRUCTIONS)
            self.view.save_bt.config(state='normal')
            self.view.delete_bt.config(state=tkinter.DISABLED)
            self.view.update_bt.config(state=tkinter.DISABLED)
            self.view.persistence_status['text'] = ''
        except Exception as e:
            self.handle_exception('', e)

    def _save_translation(self, _):
        if self.view.save_bt['state'] == tkinter.DISABLED:
            return
        try:
            user_input = super().get_user_input()
            trans_text = self.view.output_frame.get("1.0", tkinter.END)
            status_msg = self.model.save_translation(user_input, trans_text)
            super().update_status(status_msg)
        except Exception as e:
            self.handle_exception('Save error: ', e)

    def _on_closing(self):
        self.model.save_dictionary()
        self.view.stop()

    def bind_translation_controls(self):
        self.view.clear_bt.bind("<Button-1>", super().clear_screen)
        self.view.swap_languages_bt.bind("<Button-1>", self._swap_languages)
        self.view.destination_language.bind("<<ComboboxSelected>>", self._update_transliteration)
        self.view.trans_bt.bind("<Button-1>", self._translate_text)
        self.view.save_bt.bind("<Button-1>", self._save_translation)
        self.view.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


class PersistenceController(Controller):

    def _handle_persistence_error(self, e):
        self.handle_exception('Persistence error: ', e)
        self.view.persistence_status['text'] = 'See error below or in log file'

    def _populate_all_widgets(self, status_msg, persistence_msg, translation):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        Controller.set_check_button(self.view.add_transliteration_check_bt, translation['is_add_transliteration'])
        Controller.set_check_button(self.view.add_source_check_bt, translation['is_add_src'])
        self.view.save_bt.config(state=tkinter.DISABLED)
        self.view.input_frame.insert(tkinter.END, translation['text_lines'])
        self.view.output_frame.insert(tkinter.END, translation['translated_text'])
        status_msg = status_msg + ';  may change text and click Update, or click Delete'
        super().update_status(status_msg)

        self.delete_bt_click_count = 0
        self.view.persistence_status['text'] = persistence_msg
        self.view.delete_bt.config(state=tkinter.NORMAL)
        self.view.update_bt.config(state=tkinter.NORMAL)

    def _next_translation(self, _):
        try:
            status_msg, persistence_msg, translation = self.model.next_translation()
            self._populate_all_widgets(status_msg, persistence_msg, translation)
        except Exception as e:
            self._handle_persistence_error(e)

    def _previous_translation(self, _):
        try:
            status_msg, persistence_msg, translation = self.model.previous_translation()
            self._populate_all_widgets(status_msg, persistence_msg, translation)
        except Exception as e:
            self._handle_persistence_error(e)

    def _update_translation(self, _):
        if self.view.delete_bt['state'] == tkinter.DISABLED:
            return
        try:
            user_input = self.get_user_input()
            trans_text = self.view.output_frame.get("1.0", tkinter.END)
            status_msg, persistence_msg = self.model.persistence.update_translation(user_input, trans_text)
            super().update_status(status_msg)
            self.view.persistence_status['text'] = persistence_msg
        except Exception as e:
            self._handle_persistence_error(e)

    def _delete_translation(self, _):
        if self.view.update_bt['state'] == tkinter.DISABLED:
            return
        self.delete_bt_click_count += 1
        try:
            if self.delete_bt_click_count == 1:
                self.view.persistence_status['text'] = f'Click Delete again, \u25BA \u25C4 Clear to cancel.'
            else:
                status_msg, persistence_msg = self.model.persistence.delete_translation()
                assert status_msg in self.view.status_label['text']
                self.view.status_label['text'] = status_msg
                self.view.persistence_status['text'] = persistence_msg
                self.delete_bt_click_count == 0
        except Exception as e:
            self._handle_persistence_error(e)

    def bind_persistence_controls(self):
        self.view.next_bt.bind("<Button-1>", self._next_translation)
        self.view.previous_bt.bind("<Button-1>", self._previous_translation)
        self.view.update_bt.bind("<Button-1>", self._update_translation)
        self.view.delete_bt.bind("<Button-1>", self._delete_translation)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


def language_names(config: dict) -> list:
    lang_names = [v for v, _ in LANGUAGE_NAMES_ABBR.items()]
    top_of_list = config.get('TOP_OF_LIST_LANGUAGES').split(',')
    return top_of_list + [x for x in lang_names if x not in top_of_list]


def main():
    try:
        with open(os.path.dirname(__file__) + "/config_trans.json") as f:
            config = json.load(f)
        set_logger(config)
        if log.isEnabledFor(logging.DEBUG):
            log.info(f'Transliterate languages: {TRANSLITERATE_LANGUAGE_NAMES}')

        lang_names = language_names(config)
        v = View(lang_names, Config.TRANSLATE_INSTRUCTIONS)

        google_translator = googletrans.Translator()
        persistence = FilePersistence(config)
        m = Model(config, google_translator, persistence)

        c = TranslationController(v, m)
        c.bind_translation_controls()
        c2 = PersistenceController(v, m)
        c2.bind_persistence_controls()

        log.info('>>> Starting view')
        v.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        log.error(exc_trace)


if __name__ == '__main__':
    main()
