from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from states import TEST, STATISTICS, SETTINGS, CHOOSING


def start_command(update: Update, context: CallbackContext):
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Начать тест', callback_data=str(TEST))],
        [InlineKeyboardButton('Статистика', callback_data=str(STATISTICS))],
        [InlineKeyboardButton('Настройки', callback_data=str(SETTINGS))],
    ])
    update.message.reply_text('こんにちは!\n Выбери, что нужно сделать.', reply_markup=keyboard_markup)

    return CHOOSING