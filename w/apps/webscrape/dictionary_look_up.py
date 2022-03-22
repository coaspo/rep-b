#!/usr/bin/env python3
import requests
import json

DICTIONARY_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
DEBUG = True


def get_user_word_input():
    print('\n__Enter word(s) \
      \n____add dash (-) prefix to first word to suppress example/origin,\
      \n____hit Enter twice when done,\
      \n__Or enter a non-letter and Enter to exit.\n')
    words = []
    definition_only = False
    while True:
        line = input()
        if line == '' or (len(line) == 1 and not line[0].isalpha()):
            break
        if line[0] == '-':
            definition_only = True
            line = line[1:]
        multi_words = line.split(" ")
        for word in multi_words:
            word = word.strip()
            if word != '':
                if not word.isalpha():
                    print('Rejected invalid word:', word)
                    continue
                words.append(word)
    if DEBUG:
        print('definition_only=', definition_only, '\n  words=', words)
    return definition_only, words


def get_dictionary_page(word: str):
    url = DICTIONARY_URL + word
    page = requests.get(url, headers='')
    text = page.text
    if DEBUG:
        print('text=', text)
    return text


def parse_json_definition(text: str):
    try:
        d = json.loads(text)[0]
    except Exception as exc:
        print(exc)
        return '??', '??', '??'
    definitions = d["meanings"][0]["definitions"][0]
    definition = definitions["definition"]
    example = definitions["example"] if 'example' in definitions.keys() \
        else '-'
    origin = d["origin"] if 'origin' in d.keys() \
        else '-'
    if DEBUG:
        print('definition=', definition, '\n  example=', example, '\n  origin=', origin)
    return definition, example, origin


def lookup_definitions(words: list):
    definitions = []
    examples = []
    origins = []
    for word in words:
        text = get_dictionary_page(word)
        definition, example, origin = parse_json_definition(text)
        definitions.append(definition)
        examples.append(example)
        origins.append(origin)
    if DEBUG:
        print('definitions=', definitions, '\n  examples=', examples, '\n  origins=', origins)
    return definitions, examples, origins


def print_definitions(words, definitions, *args):
    for i in range(len(words)):
        print(words[i], ':', definitions[i])
        if len(args) == 0:
            continue
        is_definition_only = args[0][i] == '-'
        if is_definition_only or definitions[i] == '??':
            continue
        print(' ' * len(words[i]), ' example:', args[0][i])
        print(' ' * len(words[i]), ' origin:', args[1][i])


def main():
    try:
        while True:
            definition_only, words = get_user_word_input()
            if len(words) == 0:
                print('Done')
                exit(0)
            definitions, examples, origins = lookup_definitions(words)
            if definition_only:
                print_definitions(words, definitions)
                continue
            print_definitions(words, definitions, examples, origins)
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
