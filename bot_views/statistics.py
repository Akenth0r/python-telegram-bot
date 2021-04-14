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
        output = ""
        for word in words:
            output += f'{word.original}\n'
        directory = os.path.join(str(update['base_path']), 'tmp')
        directory = os.path.join(directory, f'{chat_id}.pdf')
        file_system_helper.save_to_file(directory, output)
        print(file_system_helper.is_file_exist(directory))
        bot_instance.answer_callback_query(update['callback_query']['id'])
        print(f'directory is {directory}')
        print(bot_instance.send_document(chat_id, f'http://baban-bot.herokuapp.com/download/{chat_id}.pdf').content)

        return

    else:
        output = "Вы не выучили ни одного слова"

    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.send_message(chat_id, reply_to_message_id=message_id, text=output)

    # Возвращаемся на главный экран
    start.restart(update, bot_instance)
