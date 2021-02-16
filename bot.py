import requests
import json
import telegram_api as api

# _handlers = ["methodName":  function, ...]
class Bot:

    def __init__(self, token):
        self.token = token
        self._bot_url = f"https://api.telegram.org/bot{self.token}"
        # Разные меню имя/пункты
        self._menus = {}
        # Обработчики команд/сообщений
        self._handlers = {}

    def handle_message(self, message):
        if message['text'] in self._handlers.keys():
            self._handlers[message['text']](message)

    def send_message(self, chat_id, text, keyboard_array=None, reply_to_message_id=None):
        data = {"chat_id": chat_id, "text": text}
        if keyboard_array is not None:
            data["reply_markup"] = api.reply_keyboard(keyboard_array)
        if reply_to_message_id is not None:
            data["reply_to_message_id"] = reply_to_message_id
        api.telegram_method(api.METHOD_SEND_MESSAGE, data, self._bot_url)

    def add_menu(self, menu):
        pass

    def add_handler(self, command, handler):
        print(f'registered command {command}')
        self._handlers[command] = handler

    def remove_handler(self, command):
        pass


class Settings:
    def __init__(self, settings={}):
        self._settings = settings

   # Установить настройку
    def set(self, key, value):
        pass

    # Получить настройку
    def get(self, key, value):
        pass

    # Сохраняем что-то
    def save(self):
        pass