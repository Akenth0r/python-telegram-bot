from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import states
from db import User, UserSettings, UserStatistics, get_user
from bot_views import start


def settings_start(update: Update, context: CallbackContext):

    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'Тему', callback_data=f'{states.SET_THEME}')],
        [InlineKeyboardButton(f'Количество вопросов в тесте', callback_data=f'{states.SET_SESSION_WORDS_COUNT}')],
        [InlineKeyboardButton(f'Необходимое количество правильных ответов', callback_data=f'{states.SET_RIGHT_ANSWER_COUNT}')],
        [InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])

    update.callback_query.message.edit_text('Выбери что хочешь изменить:', reply_markup=keyboard_markup)
    return states.SETTINGS


def set_theme_menu(update: Update, context: CallbackContext):
    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'Животные', callback_data='animals')],
        [InlineKeyboardButton(f'Еда', callback_data='food')],
        [InlineKeyboardButton(f'Назад', callback_data=f'{states.SETTINGS}'),
         InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])

    update.callback_query.message.edit_text('Темы:', reply_markup=keyboard_markup)
    return states.SET_THEME


def set_right_answer_count_menu(update: Update, context: CallbackContext):
    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'1', callback_data='1'),
         InlineKeyboardButton(f'3', callback_data='3'),
         InlineKeyboardButton(f'5', callback_data='5')],
        [InlineKeyboardButton(f'7', callback_data='7'),
         InlineKeyboardButton(f'10', callback_data='10'),
         InlineKeyboardButton(f'15', callback_data='15')],
        [InlineKeyboardButton(f'Назад', callback_data=f'{states.SETTINGS}'),
         InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])

    update.callback_query.message.reply_text('Количество правильных ответов:', reply_markup=keyboard_markup)
    return states.SET_RIGHT_ANSWER_COUNT


def set_session_words_count_menu(update: Update, context: CallbackContext):
    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'1', callback_data='1'),
         InlineKeyboardButton(f'3', callback_data='3'),
         InlineKeyboardButton(f'5', callback_data='5')],
        [InlineKeyboardButton(f'7', callback_data='7'),
         InlineKeyboardButton(f'10', callback_data='10'),
         InlineKeyboardButton(f'15', callback_data='15')],
        [InlineKeyboardButton(f'Назад', callback_data=f'{states.SETTINGS}'),
         InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])

    update.callback_query.message.reply_text('Количество вопросов в тесте:', reply_markup=keyboard_markup)
    return states.SET_SESSION_WORDS_COUNT


def set_theme(update: Update, context: CallbackContext):
    # Получаем или создаем пользователя
    user = get_user(update.callback_query.message.chat_id)
    print(f'Чат id{update.callback_query.message.chat_id}')

    # Изменяем настройки пользователя
    user.settings.theme_id = update.callback_query.data
    user.save()

    # Возвращаемся на главный экран
    start.restart(update)
    return states.CHOOSING


def set_right_answer_count(update: Update, context: CallbackContext):
    # Получаем или создаем пользователя
    user = get_user(update.callback_query.message.chat_id)
    print(f'Чат id{update.callback_query.message.chat_id}')

    # Изменяем настройки пользователя
    user.settings.right_answer_count = update.callback_query.data
    print('Изменили right answer')
    user.save()

    # Возвращаемся на главный экран
    start.restart(update)
    return states.CHOOSING


def set_session_words_count(update: Update, context: CallbackContext):
    # Получаем или создаем пользователя
    user = get_user(update.callback_query.message.chat_id)
    print(f'Чат id{update.callback_query.message.chat_id}')

    # Изменяем настройки пользователя
    user.settings.session_words_count = update.callback_query.data
    print('Изменили session words')
    user.save()

    # Возвращаемся на главный экран
    start.restart(update)
    return states.CHOOSING
