from datetime import datetime

import repeat_config
from db import get_user, get_user_words_to_repeat_count


def notify(update, bot_instance):
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button('Повторить', callback_data='@repeat')],
        [bot_instance.inline_keyboard_button('Повторить позже', callback_data='@repeatAfter')],
    ])
    bot_instance.send_message(update['message']['chat']['id'], 'Привет!\nТебе пора повторять слова',
                              reply_to_message_id=update['message']['message_id'], reply_markup=keyboard_markup)


def repeat_after(update, bot_instance):
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    user = get_user(update['callback_query']['message']['chat']['id'])
    user.last_session = datetime.utcnow()
    user.save()
    bot_instance.edit_message_text(chat_id, message_id=message_id,
                                   text=f'Отлично, напомню тебе через {repeat_config.USER_REPEAT_PERIOD} минут!')

def repeat(update, bot_instance):
    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.send_message(update['callback_query']['message']['chat']['id'], 'Функционал в разработке у Никиты')

def repeat_count(update, bot_instance):
    count = get_user_words_to_repeat_count(update['message']['chat']['id'])
    bot_instance.send_message(update['message']['chat']['id'], text=f'Words count is {count}')