from ltrans.persistence import Persistence
from ltrans.reference import LANGUAGE_NAMES_ABBR
from ltrans.reference import TRANSLITERATE_LANGUAGE_NAMES
from ltrans.util import NON_LETTERS_REGEX
from ltrans.userinput import UserInput
import googletrans
import json
import logging
import os.path
import random
import re
import transliterate
import unicodedata

log = logging.getLogger(__name__)


class Dictionary(dict):
    def __init__(self, config: dict, src_language: str, dest_language: str):
        self._src_language = src_language
        self._dest_language = dest_language
        self._set_file_path(config, src_language, dest_language)

        if os.path.isfile(self._dict_file_path):
            with open(self._dict_file_path, "r", encoding='utf8') as f:
                dictionary = json.load(f)
        else:
            dictionary = {}
        super(Dictionary, self).__init__(dictionary)

        self._initial_len = len(self.keys())

    def _set_file_path(self, config: dict, src_language: str, dest_language: str):
        if config is None or config.get('DICTIONARY_DIR') is None:
            raise Exception('config missing config parameter "DICTIONARY_DIR"')
        dictionary_dir = config['DICTIONARY_DIR']

        if dictionary_dir.startswith("./"):
            dictionary_dir = os.path.dirname(__file__) + dictionary_dir[1:]
            if not os.path.exists(dictionary_dir):
                os.mkdir(dictionary_dir, 0o755)
        elif not os.path.isdir(dictionary_dir):
            raise Exception(f'config parameter DICTIONARY_DIR={dictionary_dir} is and invalid directory')
        self._dict_file_path = dictionary_dir + '/' + src_language + dest_language + '-dict.json'
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'dict_file_path={self._dict_file_path}')

    @property
    def src_language(self) -> str:
        return self._src_language

    @property
    def dest_language(self) -> str:
        return self._dest_language

    def words(self) -> dict:
        return {k: v for k, v in self.items()}

    def save(self):
        current_len = len(self.keys())
        len_diff = current_len - self._initial_len
        if len_diff > 0:
            with open(self._dict_file_path, "w", encoding='utf8') as f:
                json.dump(self, f, ensure_ascii=False, sort_keys=True, indent=0)
            if log.isEnabledFor(logging.DEBUG):
                current_len = len(self.keys())
                sample_words = random.sample(self.items(), min(4, current_len))
                log.debug(
                    f'initial/current word count: {self._initial_len}/{current_len} ' +
                    f' 4-word random sample: {sample_words}')
            self._initial_len = current_len
            log.info(f'{len_diff} new words were added to: {os.path.basename(self._dict_file_path)}')

    def __str__(self):
        current_len = len(self.keys())
        sample_words = random.sample(self.items(), min(4, current_len))
        return 'Dictionary: ' + str(sample_words) + '...'


class Model:
    def __init__(self, config: dict, google_translator: googletrans.client.Translator, persistence: Persistence):
        self._config = config
        self._persistence = persistence
        self._dictionary = None
        self._translator = google_translator
        self._last_translated_text = None

    @property
    def persistence(self) -> Persistence:
        return self._persistence

    def translate(self, user_input: UserInput) -> str:
        if self._dictionary is None \
                or user_input.src_language != self._dictionary.src_language \
                or user_input.destination_language != self._dictionary.dest_language:
            self._dictionary = Dictionary(self._config, user_input.src_language, user_input.destination_language)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(user_input)
        self._last_translated_text = translate_text(user_input, self._dictionary, self._translator)
        return self._last_translated_text

    def save_translation(self, user_input: UserInput, translated_text: str) -> str:
        status_msg = self.persistence.save_translation(user_input, translated_text)
        return status_msg

    def next_translation(self) -> tuple:
        status_msg, persistence_msg, translation = self.persistence.next_translation()
        return status_msg, persistence_msg, translation

    def previous_translation(self) -> tuple:
        status_msg, persistence_msg, translation = self.persistence.previous_translation()
        return status_msg, persistence_msg, translation

    def delete_translation(self) -> tuple:
        status_msg, persistence_msg = self.persistence.delete_translation()
        return status_msg, persistence_msg

    def update_translation(self, user_input: UserInput, translated_text: str) -> tuple:
        status_msg, persistence_msg = self.persistence.update_translation(user_input, translated_text)
        return status_msg, persistence_msg

    def save_dictionary(self):
        if self._dictionary is not None:
            self._dictionary.save()


def translate_text(user_input: UserInput, dictionary: Dictionary, translator: googletrans.client.Translator) -> str:
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'user_input={user_input}, dictionary={str(dictionary)}')
    input_lines = user_input.text_lines.split('\n')
    translated_lines = [translate_line(line, dictionary, translator) for line in input_lines]
    translated_lines = possibly_add_extra_lines(input_lines, translated_lines, user_input)
    trans_text = '\n'.join(translated_lines).strip()
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'trans_text={trans_text}')
    return trans_text


def possibly_add_extra_lines(input_lines: list, translated_lines: list, user_input: UserInput) -> list:
    output_lines = None
    if user_input.is_add_src:
        output_lines = input_lines.copy()
        if user_input.is_add_transliteration:
            transliteration_lines = transliterate_lines(input_lines, user_input.src_language)
            if transliteration_lines is not None and transliteration_lines != []:
                output_lines = [a + '\n' + b for a, b in zip(output_lines, transliteration_lines)]

    if output_lines is None:
        output_lines = translated_lines
    else:
        output_lines = [a + '\n' + b for a, b in zip(output_lines, translated_lines)]

    if user_input.is_add_transliteration:
        transliteration_lines = transliterate_lines(translated_lines, user_input.destination_language)
        if transliteration_lines is not None and transliteration_lines != []:
            output_lines = [a + '\n' + b for a, b in zip(output_lines, transliteration_lines)]

    if output_lines != translated_lines:
        output_lines = [line + '\n' for line in output_lines]
    return output_lines


def transliterate_lines(lines: list, lines_language: str) -> list:
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'  lines_language={lines_language}')
    if lines_language not in TRANSLITERATE_LANGUAGE_NAMES:
        return []
    lang_abbr = LANGUAGE_NAMES_ABBR[lines_language]
    return [transliterate.translit(line, lang_abbr, reversed=True) for line in lines]


def translate_line(line: str, dictionary: Dictionary, translator: googletrans.client.Translator) -> str:
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'  line={line}, translator={str(translator)}')
    line_w_lrs_and_spaces = re.sub(NON_LETTERS_REGEX, '', line.rstrip())
    words = line_w_lrs_and_spaces.split()
    words = [x for x in words if len(x) > 0]
    trans_line = re.sub("'([^ ]+)", r'\1', line)
    for word in words:
        translated_word = translate_word(word, dictionary, translator)
        trans_line = re.sub(word, translated_word, trans_line, 1)
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'   trans_line={trans_line}')
    return trans_line


def translate_word(word: str, dictionary: Dictionary, translator: googletrans.client.Translator) -> str:
    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            f'    word={word}, src_language={dictionary.src_language}, dest_language={dictionary.dest_language},' +
            f' translator={str(translator)}')
    no_accent_word = strip_accents(word)
    translated_word = dictionary.get(no_accent_word)
    if translated_word is None:
        translated_word = dictionary.get(no_accent_word[0:1].upper() + no_accent_word[1:])
    if translated_word is None:
        translated_word = dictionary.get(no_accent_word[0:1].lower() + no_accent_word[1:])
    if translated_word is None:
        src_language_abbr = LANGUAGE_NAMES_ABBR[dictionary.src_language]
        dest_language_abbr = LANGUAGE_NAMES_ABBR[dictionary.dest_language]
        print('---', word)
        print('---', src_language_abbr)
        print('---', dest_language_abbr)
        print('-  -  -', translator)
        
        translation = translator.translate(word, src=src_language_abbr, dest=dest_language_abbr)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'      translation={translation}')
        translated_word = translation.text
        if word != translated_word:
            dictionary[word] = translated_word.lower()
        # translation.transliteration is always none , need google account?
    if word[0:1].isupper():
        w = translated_word[0:1].upper() + translated_word[1:]
        translated_word = w  # to avoid repeating first ltr (?)
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f'     translated_word={translated_word}')
    return translated_word


def strip_accents(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
