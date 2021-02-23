from typing import List


# Слово темы
class ThemeWord:
    def __init__(self, original: str = '', translation: str = ''):
        self.original = original
        self.translation = translation

    def serialize(self):
        return {
            "original": self.original,
            "translation": self.translation,
        }

    def deserialize(self, obj: dict):
        self.original = obj['original']
        self.translation = obj['translation']


# Тема - массив слов и название
class Theme:
    def __init__(self, title: str = '', words: List[ThemeWord] = None):
        self.title = title
        self.words = words

    def add_word(self, word: ThemeWord):
        self.words.append(word)

    def save(self):
        pass

    def load(self, theme_title: str):
        pass

    def serialize(self):
        res = {'title': self.title, 'words': []}
        for word in self.words:
            res['words'].append(word.serialize())
        return res

    def deserialize(self, obj):
        self.title = obj['title']
        self.words = []
        for word in obj['words']:
            new_word = ThemeWord()
            new_word.deserialize(word)
            self.words.append(new_word)