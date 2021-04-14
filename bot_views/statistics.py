import os

import file_system_helper
import states
from db import User, get_user, get_user_remembered_words
from bot_views import start


def show_statistics(update, bot_instance):
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    user = get_user(chat_id)
    stats = user.statistics

    words = get_user_remembered_words(user)
    if len(words):
        output = "Слова, которые вы выучили: \n"
        for word in words:
            output += f'{word.original} - {word.translation}\n'
        directory = os.path.join(update['base_path'], ['download', user.id])
        file_system_helper.save_to_file(directory, output)
        bot_instance.send_document(chat_id, output)
    else:
        output = "Вы не выучили ни одного слова"

    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.send_message(chat_id, reply_to_message_id=message_id, text=output)

    # Возвращаемся на главный экран
    start.restart(update, bot_instance)
