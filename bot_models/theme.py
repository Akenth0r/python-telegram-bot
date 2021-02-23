from typing import List

import constants
import file_system_helper
import os


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
        if obj is None:
            return False
        self.original = obj['original']
        self.translation = obj['translation']
        return True


# Тема - массив слов и название
class Theme:
    def __init__(self, title: str = '', words: List[ThemeWord] = None):
        self.title = title
        self.words = words

    def add_word(self, word: ThemeWord):
        self.words.append(word)

    def save(self):
        # Получаем путь до папки с темами
        filepath = os.path.sep.join([constants.BASE_PATH, 'data', 'themes', f'{self.title}.json'])
        # Сохраняем
        file_system_helper.save_to_file(filepath, self.serialize())

    # Загрузить тему из файла
    def load(self, theme_title: str):
        # Получаем путь до папки с темами
        filepath = os.path.sep.join([constants.BASE_PATH, 'data', 'themes', f'{theme_title}.json'])
        # Загружаем в словарь
        obj = file_system_helper.load_from_file(filepath)
        # Спокойненько десериализуем объект
        return self.deserialize(obj)

    def serialize(self):
        res = {'title': self.title, 'words': []}
        for word in self.words:
            res['words'].append(word.serialize())
        return res

    def deserialize(self, obj):
        if obj is None:
            return False
        self.title = obj['title']
        self.words = []
        for word in obj['words']:
            new_word = ThemeWord()
            new_word.deserialize(word)
            self.words.append(new_word)
        return True
