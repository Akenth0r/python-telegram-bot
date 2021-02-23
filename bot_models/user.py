# Настройки пользователя
import os

import constants
import file_system_helper


# TODO: когда начнем работать с базами данных, добавить второстепенным моделям интерфейс save/load
class UserSettings:
    def __init__(self, theme_id=None, right_answer_count=1, session_words_count=5):
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
        self.theme_id = obj['theme_id']
        self.right_answer_count = obj['right_answer_count']
        self.session_words_count = obj['session_words_count']


# Статистика пользователя
class UserStatistics:
    def __init__(self, words_remembered=0, words_left=0):
        self.words_remembered = words_remembered
        self.words_left = words_left

    # Преобразовать модель в словарь
    def serialize(self):
        return {
            "words_remembered": self.words_remembered,
            "words_left": self.words_left,
        }

    def deserialize(self, obj: dict):
        self.words_left = obj['words_left']
        self.words_remembered = obj['words_remembered']


# Пользователь
class User:
    def __init__(self, user_id, settings: UserSettings = None, statistics: UserStatistics = None):
        self.user_id = user_id
        self.settings = settings
        self.statistics = statistics

    def save(self):
        # Получаем путь до папки с темами
        filepath = os.path.sep.join([constants.BASE_PATH, 'data', 'users', f'{self.user_id}.json'])
        # Сохраняем
        file_system_helper.save_to_file(filepath, self.serialize())

    # Пока что user_id это строка с названием файла, но в будущем, возможно, всё изменится...
    def load(self, user_id: str):
        # Получаем путь до папки с темами
        filepath = os.path.sep.join([constants.BASE_PATH, 'data', 'users', f'{user_id}.json'])
        # Загружаем в словарь
        obj = file_system_helper.load_from_file(filepath)
        # Спокойненько десериализуем объект
        self.deserialize(obj)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "settings": self.settings.serialize(),
            "statistics": self.statistics.serialize(),
        }

    def deserialize(self, obj: dict):
        self.user_id = obj['user_id']

        self.settings = UserSettings()
        self.settings.deserialize(obj['settings'])

        self.statistics = UserStatistics()
        self.statistics.deserialize(obj['statistics'])
