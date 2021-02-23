from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

import states


def test_begin(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Начинаем наш тест...")
    return states.TEST


def test(update: Update, context: CallbackContext):
    # Вот тут мы подгружаем слова по теме и считаем число правильных ответов
    pass
    return states.TEST


def test_end(update: Update, context: CallbackContext):
    pass
