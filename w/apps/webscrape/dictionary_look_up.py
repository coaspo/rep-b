#!/usr/bin/env python3

import requests
import json

DICTIONARY_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


def input_words():
    words = []
    while True:
      line = input()
      if line == '' or not line[0].isalpha():
        break
      multi_words = line.split(" ")
      for word in multi_words:
        word = word.strip()
        if word != '':
          if not word.isalpha():
            break
          words.append(word)
    return words

def get_dictionary_page(word: str):
    url = DICTIONARY_URL + word
    page = requests.get(url, headers='')
    return page.text

def parse_definition(text: str):
    d =json.loads(text)[0]
    definition = d["meanings"][0]["definitions"][0]["definition"]
    return definition

def lookup_definitions(words: list):
    definitions = []
    for word in words:
      text = get_dictionary_page(word)
      definition = parse_definition(text)
      definitions.append(definition)
    return definitions

def main():
    try:
        while True:
          print ('\n Enter word(s), space or new line delimited,\n\
      or a non-letter to exit.\n')
          words = input_words()
          if len(words) == 0:
            exit(0)
          definitions = lookup_definitions(words)
          for i in range(len(words)):
            print(words[i], ': ',  definitions[i])
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
