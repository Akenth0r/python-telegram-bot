from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot_models.user import User, UserSettings, UserStatistics
from states import TEST, STATISTICS, SETTINGS, CHOOSING


def start_command(update: Update, context: CallbackContext):
    # Запомнить пользователя, если не запомнен
    user = User()
    if not user.load(str(update.message.chat_id)):
        user.user_id = update.message.chat_id
        user.settings = UserSettings()
        user.statistics = UserStatistics()
        user.save()

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Начать тест', callback_data=str(TEST))],
        [InlineKeyboardButton('Статистика', callback_data=str(STATISTICS))],
        [InlineKeyboardButton('Настройки', callback_data=str(SETTINGS))],
        [InlineKeyboardButton('Выдача лоли', callback_data=str(777))],
    ])
    update.message.reply_text('こんにちは!\n Выбери, что нужно сделать.', reply_markup=keyboard_markup)

    return CHOOSING