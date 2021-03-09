from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot_models.user import User, UserSettings, UserStatistics
from states import TEST, STATISTICS, SETTINGS, CHOOSING


def start_command(update: Update, context: CallbackContext):
    # Запомнить пользователя, если не запомнен
    user = User()
    if not user.load_or_init(str(update.message.chat_id)):
        print('Это новый юзер')

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Начать тест', callback_data=str(TEST))],
        [InlineKeyboardButton('Статистика', callback_data=str(STATISTICS))],
        [InlineKeyboardButton('Настройки', callback_data=str(SETTINGS))],
        # [InlineKeyboardButton('Выдача лоли', callback_data=str(777))],
    ])

    update.message.reply_text('こんにちは!\n Выбери, что нужно сделать.', reply_markup=keyboard_markup)
    return CHOOSING


def restart(update: Update, context: CallbackContext = None):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Начать тест', callback_data=str(TEST))],
        [InlineKeyboardButton('Статистика', callback_data=str(STATISTICS))],
        [InlineKeyboardButton('Настройки', callback_data=str(SETTINGS))],
    ])
    update.callback_query.message.reply_text('こんにちは!\n Выбери, что нужно сделать.', reply_markup=keyboard_markup)
    return CHOOSING
