# Настройки пользователя
import os
from typing import List

import constants
import file_system_helper


# TODO: когда начнем работать с базами данных, добавить второстепенным моделям интерфейс save/load
class UserSettings:
    def __init__(self, theme_id='animals', right_answer_count=1, session_words_count=5):
        self.theme_id = theme_id
        self.right_answer_count = right_answer_count
        self.session_words_count = session_words_count

    def serialize(self):
        return {
            "theme_id": self.theme_id,
            "right_answer_count": self.right_answer_count,
            "session_words_count": self.session_words_count,
        }

    def deserialize(self, obj: dict):
        if obj is None:
            return False
        self.theme_id = obj['theme_id']
        self.right_answer_count = obj['right_answer_count']
        self.session_words_count = obj['session_words_count']
        return True


# class UserStatisticsRememberedWord:
#     def __init__(self, word: str = '', right_answer_count: int = 0):
#         self.word = word
#         self.right_answer_count = right_answer_count
#
#     def serialize(self):
#         return {
#             "word": self.word,
#             "right_answer_count": self.right_answer_count
#         }
#
#     def deserialize(self, obj: dict):
#         if obj is None:
#             return False
#         self.word = obj['word']
#         self.right_answer_count = obj['right_answer_count']
#         return True


# Статистика пользователя
class UserStatistics:
    def __init__(self, remembered_words_count=0, words_left=0,
                 remembered_words_list: dict = None):
        if remembered_words_list is None:
            remembered_words_list = {}
        self.words_remembered = remembered_words_count
        self.words_left = words_left
        self.remembered_words_list = remembered_words_list

    # Преобразовать модель в словарь
    def serialize(self):
        res = {
            "remembered_words_count": self.words_remembered,
            "words_left": self.words_left,
            "remembered_words_list": {},
        }
        for key in self.remembered_words_list:
            res['remembered_words_list'].setdefault(key, self.remembered_words_list[key])
        return res

    def deserialize(self, obj: dict):
        if obj is None:
            return False
        self.words_left = obj['words_left']
        self.words_remembered = obj['remembered_words_count']
        self.remembered_words_list = {}
        for key in obj['remembered_words_list']:
            #remembered_word = UserStatisticsRememberedWord()
            #remembered_word.deserialize(word)
            self.remembered_words_list.setdefault(key, obj['remembered_words_list'][key])

        return True


# Пользователь
class User:
    def __init__(self, user_id=None, settings: UserSettings = None, statistics: UserStatistics = None):
        self.user_id = user_id
        self.settings = settings
        self.statistics = statistics

    def save(self):
        # Получаем путь до папки с юзерами
        filepath = os.path.sep.join([constants.BASE_PATH, 'data', 'users', f'{self.user_id}.json'])
        # Сохраняем
        file_system_helper.save_to_file(filepath, self.serialize())

    # Пока что user_id это строка с названием файла, но в будущем, возможно, всё изменится...
    def load_or_init(self, user_id: str):
        # Получаем путь до папки с юзерами
        filepath = os.path.sep.join([constants.BASE_PATH, 'data', 'users', f'{user_id}.json'])
        # Загружаем в словарь
        obj = file_system_helper.load_from_file(filepath)
        # Спокойненько десериализуем объект
        success = self.deserialize(obj)
        # Создаем новый если не получилось
        if not success:
            self.user_id = user_id
            self.settings = UserSettings()
            self.statistics = UserStatistics()
            self.save()
        return success

    def serialize(self):
        settings = None
        if self.settings is not None:
            settings = self.settings.serialize()
        statistics = None
        if self.statistics is not None:
            statistics = self.statistics.serialize()
        return {
            "user_id": self.user_id,
            "settings": settings,
            "statistics": statistics,
        }

    def deserialize(self, obj: dict):
        if obj is None:
            return False
        self.user_id = obj['user_id']

        self.settings = UserSettings()
        self.settings.deserialize(obj['settings'])

        self.statistics = UserStatistics()
        self.statistics.deserialize(obj['statistics'])
        return True
