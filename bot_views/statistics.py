from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

import states
from db import User, get_user
from bot_views import start


def show_statistics(update: Update, context: CallbackContext):
    user = get_user(update.callback_query.message.chat_id)
    stats = user.statistics

    word_dict = stats.remembered_words
    right_count = user.settings.right_answer_count
    known_count = 0
    for word in word_dict:
        if int(word.right_answer_count) >= right_count:
            known_count += 1

    update.callback_query.message.edit_text(f'Вы выучили {known_count} слов(а)')

    # Возвращаемся на главный экран
    start.restart(update)
