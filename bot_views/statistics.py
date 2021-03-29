import states
from db import User, get_user
from bot_views import start


def show_statistics(update, bot_instance):
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    user = get_user(chat_id)
    stats = user.statistics

    word_dict = stats.remembered_words
    right_count = user.settings.right_answer_count
    known_count = 0
    for word in word_dict:
        if int(word.right_answer_count) >= right_count:
            known_count += 1


    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.edit_message_text(chat_id, message_id=message_id, text=f'Вы выучили {known_count} слов(а)')


    # Возвращаемся на главный экран
    start.restart(update, bot_instance)
