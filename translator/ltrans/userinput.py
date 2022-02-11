class UserInputError(Exception):
    pass


class UserInput:
    def __init__(self, text_lines: str, src_language: str, dest_language: str, is_add_src: bool,
                 is_add_transliteration: bool):
        self._text_lines = text_lines
        self._src_language = src_language
        self._dest_language = dest_language
        self._is_add_src = is_add_src
        self._is_add_transliteration = is_add_transliteration

    @property
    def text_lines(self) -> str:
        return self._text_lines

    @property
    def destination_language(self) -> str:
        return self._dest_language

    @property
    def src_language(self) -> str:
        return self._src_language

    @property
    def is_add_src(self) -> bool:
        return self._is_add_src

    @property
    def is_add_transliteration(self) -> bool:
        return self._is_add_transliteration

    def __str__(self) -> str:
        return f'UserInput: src = {self.src_language},  dest = {self.destination_language}, ' + \
               f' is_add_src = {self.is_add_src},  is_add_transliteration = {self.is_add_transliteration}, ' + \
               f' text = {self.text_lines} '
