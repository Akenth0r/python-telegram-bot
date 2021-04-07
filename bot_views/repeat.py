from datetime import datetime, timedelta

import repeat_config
from bot_views import test
from db import get_user, get_user_words_to_repeat_count, get_user_remembered_words, User


def notify(update, bot_instance):
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button('Повторить', callback_data='@repeat')],
        [bot_instance.inline_keyboard_button('Повторить позже', callback_data='@repeatAfter')],
    ])
    user = get_user(update['message']['chat']['id'])
    words_to_repeat_count = get_user_words_to_repeat_count(user.id)

    if user.last_session and (datetime.utcnow() - user.last_session >= timedelta(
            minutes=repeat_config.USER_REPEAT_PERIOD)) and words_to_repeat_count >= user.settings.session_words_count:
        get_user_remembered_words(user)
        bot_instance.send_message(update['message']['chat']['id'],
                                  f'Привет!\nТебе пора повторить {words_to_repeat_count} слов',
                                  reply_to_message_id=update['message']['message_id'], reply_markup=keyboard_markup)
    else:
        bot_instance.send_message(update['message']['chat']['id'],
                                  f'Время еще не пришло...')
#
# def notify_user(update, bot_instance, user: User):
#     keyboard_markup = bot_instance.inline_keyboard_markup([
#         [bot_instance.inline_keyboard_button('Повторить', callback_data='@repeat')],
#         [bot_instance.inline_keyboard_button('Повторить позже', callback_data='@repeatAfter')],
#     ])
#     words_to_repeat_count = get_user_words_to_repeat_count(user.id)
#
#     if user.last_session and (datetime.utcnow() - user.last_session) >= timedelta(
#             minutes=repeat_config.USER_REPEAT_PERIOD) and words_to_repeat_count >= user.settings.session_words_count:
#         get_user_remembered_words(user)
#         bot_instance.send_message(update['message']['chat']['id'],
#                                   f'Привет!\nТебе пора повторить {words_to_repeat_count} слов',
#                                   reply_to_message_id=update['message']['message_id'], reply_markup=keyboard_markup)


def repeat_after(update, bot_instance):
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    user = get_user(update['callback_query']['message']['chat']['id'])
    user.last_session = datetime.utcnow()
    user.save()
    bot_instance.edit_message_text(chat_id, message_id=message_id,
                                   text=f'Отлично, напомню тебе через {repeat_config.USER_REPEAT_PERIOD} минут!')


def repeat(update, bot_instance):
    test.test_begin(update, bot_instance, is_repeating=True)


def repeat_count(update, bot_instance):
    count = get_user_words_to_repeat_count(update['message']['chat']['id'])
    bot_instance.send_message(update['message']['chat']['id'], text=f'Words count is {count}')
