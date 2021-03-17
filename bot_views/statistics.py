from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

import states
from bot_models.user import User
from bot_views import start


def show_statistics(update: Update, context: CallbackContext):
    user = User()
    user.load_or_init(str(update.callback_query.message.chat_id))
    stats = user.statistics

    word_dict = stats.remembered_words_list
    right_count = int(user.settings.right_answer_count)
    known_count = 0
    for word in word_dict:
        if int(word_dict[word]) >= right_count:
            known_count += 1

    update.callback_query.message.edit_text(f'Вы выучили {known_count} слов(а)')

    # Возвращаемся на главный экран
    start.restart(update)
    return states.CHOOSING