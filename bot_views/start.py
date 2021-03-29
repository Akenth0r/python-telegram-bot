from db import User, UserSettings, UserStatistics, Session, get_user
from states import TEST, STATISTICS, SETTINGS, CHOOSING
import json


def start_command(update, bot_instance):
    # Запомнить пользователя, если не запомнен
    user = get_user(update['message']['chat']['id'])

    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button('Начать тест', callback_data=str(TEST))],
        [bot_instance.inline_keyboard_button('Статистика', callback_data=str(STATISTICS))],
        [bot_instance.inline_keyboard_button('Настройки', callback_data=str(SETTINGS))],
    ])

    bot_instance.send_message(update['message']['chat']['id'], 'Привет!\nВыбери, что нужно сделать.',
                              reply_to_message_id=update['message']['message_id'], reply_markup=keyboard_markup)


def restart(update, bot_instance):
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button('Начать тест', callback_data=str(TEST))],
        [bot_instance.inline_keyboard_button('Статистика', callback_data=str(STATISTICS))],
        [bot_instance.inline_keyboard_button('Настройки', callback_data=str(SETTINGS))],
    ])
    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.send_message(update['callback_query']['message']['chat']['id'], 'Привет!\nВыбери, что нужно сделать.',
                              reply_to_message_id=update['callback_query']['message']['message_id'], reply_markup=keyboard_markup)
    # bot.send_message(update['callback'])
    # update.callback_query.message.reply_text('こんにちは!\n Выбери, что нужно сделать.', reply_markup=keyboard_markup)
