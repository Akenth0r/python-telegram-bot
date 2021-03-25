from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import states
from db import User, UserSettings, UserStatistics, get_user
from bot_views import start


def settings_start(update: Update, context: CallbackContext):

    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'Тему', callback_data=f'{states.SET_THEME}')],
        [InlineKeyboardButton(f'Количество вопросов в тесте', callback_data=f'{states.SET_SESSION_WORDS_MENU}')],
        [InlineKeyboardButton(f'Необходимое количество правильных ответов', callback_data=f'{states.SET_RIGHT_ANSWER_MENU}')],
        [InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    update.callback_query.answer()
    update.callback_query.message.edit_text('Выбери что хочешь изменить:', reply_markup=keyboard_markup)


def set_theme_menu(update: Update, context: CallbackContext):
    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'Животные', callback_data='@th_animals')],
        [InlineKeyboardButton(f'Еда', callback_data='@th_food')],
        [InlineKeyboardButton(f'Назад', callback_data=f'{states.SETTINGS}'),
         InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    update.callback_query.answer()
    update.callback_query.message.edit_text('Темы:', reply_markup=keyboard_markup)


def set_right_answer_count_menu(update: Update, context: CallbackContext):
    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'1', callback_data='@ac_1'),
         InlineKeyboardButton(f'3', callback_data='@ac_3'),
         InlineKeyboardButton(f'5', callback_data='@ac_5')],
        [InlineKeyboardButton(f'7', callback_data='@ac_7'),
         InlineKeyboardButton(f'10', callback_data='@ac_10'),
         InlineKeyboardButton(f'15', callback_data='@ac_15')],
        [InlineKeyboardButton(f'Назад', callback_data=f'{states.SETTINGS}'),
         InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    update.callback_query.answer()
    update.callback_query.message.reply_text('Количество правильных ответов:', reply_markup=keyboard_markup)


def set_session_words_count_menu(update: Update, context: CallbackContext):
    # Формируем клавиатуру
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'1', callback_data='@wc_1'),
         InlineKeyboardButton(f'3', callback_data='@wc_3'),
         InlineKeyboardButton(f'5', callback_data='@wc_5')],
        [InlineKeyboardButton(f'7', callback_data='@wc_7'),
         InlineKeyboardButton(f'10', callback_data='@wc_10'),
         InlineKeyboardButton(f'15', callback_data='@wc_15')],
        [InlineKeyboardButton(f'Назад', callback_data=f'{states.SETTINGS}'),
         InlineKeyboardButton(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    update.callback_query.answer()
    update.callback_query.message.reply_text('Количество вопросов в тесте:', reply_markup=keyboard_markup)


def set_theme(update: Update, context: CallbackContext):
    # Получаем или создаем пользователя
    user = get_user(update.callback_query.message.chat_id)

    # Изменяем настройки пользователя
    user.settings.theme_id = update.callback_query.data.split('_')[1]
    user.save()
    update.callback_query.answer()
    # Возвращаемся на главный экран
    start.restart(update)


def set_right_answer_count(update: Update, context: CallbackContext):
    # Получаем или создаем пользователя
    user = get_user(update.callback_query.message.chat_id)

    # Изменяем настройки пользователя
    user.settings.right_answer_count = update.callback_query.data.split('_')[1]
    user.save()
    update.callback_query.answer()
    # Возвращаемся на главный экран
    start.restart(update)


def set_session_words_count(update: Update, context: CallbackContext):
    # Получаем или создаем пользователя
    user = get_user(update.callback_query.message.chat_id)

    # Изменяем настройки пользователя
    user.settings.session_words_count = update.callback_query.data.split('_')[1]
    user.save()
    update.callback_query.answer()
    # Возвращаемся на главный экран
    start.restart(update)
