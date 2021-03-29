import requests
import bot_views.start as start
import bot_views.settings as settings
import bot_views.statistics as statistics
import bot_views.test as test
import states
import json

from bot_views import repeat


class LanguageLearningBot:
    def __init__(self, token):
        self.token = token
        self._api_url = f'https://api.telegram.org/bot{token}'

    def handle_update(self, update):

        # self.updater.dispatcher.process_update(update)
        # if update['callback_query'] != None:
        #     print(update['callback_query']['message'])
        if 'message' in update:
            if 'text' in update['message'] and update['message']['text'] == '/start':
                start.start_command(update, self)
            # Тестовая штучка
            if 'text' in update['message'] and update['message']['text'] == '/repeat':
                repeat.notify(update, self)
            return

        state_map = {
            str(states.TEST): test.test_begin,
            str(states.EXIT): start.restart,
            str(states.STATISTICS): statistics.show_statistics,
            str(states.SETTINGS): settings.settings_start,
            str(states.SET_THEME): settings.set_theme_menu,
            str(states.SET_RIGHT_ANSWER_MENU): settings.set_right_answer_count_menu,
            str(states.SET_SESSION_WORDS_MENU): settings.set_session_words_count_menu,
            '@exit': start.restart,
            '@example': test.example,
            '@': test.test,
            '@ac': settings.set_right_answer_count,
            '@wc': settings.set_session_words_count,
            '@th': settings.set_theme,
            '@repeat': repeat.repeat,
            '@repeatAfter': repeat.repeat_after,
        }

        if 'callback_query' in update:
            # update.callback_query.answer('Подожди красавчик (лабу примите, пж)')
            info = update['callback_query']['data'].split('_')
            key = info[0]
            state_map[key](update, self)

    # print(update.callback_query.message)

    def set_webhook(self, url):
        data = {'url': url}

        return requests.post(f'{self._api_url}/setWebhook', data=data)

    def send_message(self, chat_id, text, reply_to_message_id=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'text': text,
            'reply_markup': reply_markup,
            'reply_to_message_id': None,
        }

        return requests.post(f'{self._api_url}/sendMessage', data=data)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False, url=None, cache_time=0):
        data = {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'url': url,
            'cache_time': cache_time,
        }

        return requests.post(f'{self._api_url}/answerCallbackQuery', data=data)

    def edit_message_text(self, chat_id, message_id=None, inline_message_id=None, text=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'text': text,
            'reply_markup': reply_markup,
        }

        return requests.post(f'{self._api_url}/editMessageText', data=data)

    def edit_message_reply_markup(self, chat_id, message_id=None, inline_message_id=None, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'reply_markup': reply_markup,
        }

        return requests.post(f'{self._api_url}/editMessageReplyMarkup')

    def inline_keyboard_markup(self, buttons: list):
        return json.dumps({
            'inline_keyboard': buttons,
        })

    def inline_keyboard_button(self, text, callback_data):
        return {
            'text': text,
            'callback_data': callback_data,
        }
