import states
from db import User, UserSettings, UserStatistics, get_user
from bot_views import start


def settings_start(update, bot_instance):
    # Формируем клавиатуру
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button(f'Тему', callback_data=f'{states.SET_THEME}')],
        [bot_instance.inline_keyboard_button(f'Количество вопросов в тесте',
                                             callback_data=f'{states.SET_SESSION_WORDS_MENU}')],
        [bot_instance.inline_keyboard_button(f'Необходимое количество правильных ответов',
                                             callback_data=f'{states.SET_RIGHT_ANSWER_MENU}')],
        [bot_instance.inline_keyboard_button(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.edit_message_text(chat_id, message_id=message_id, reply_markup=keyboard_markup,
                                   text='Выбери что хочешь изменить:')


def set_theme_menu(update, bot_instance):
    # Формируем клавиатуру
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button(f'Животные', callback_data='@th_animals')],
        [bot_instance.inline_keyboard_button(f'Еда', callback_data='@th_food')],
        [bot_instance.inline_keyboard_button(f'Назад', callback_data=f'{states.SETTINGS}'),
         bot_instance.inline_keyboard_button(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.edit_message_text(chat_id, message_id=message_id, reply_markup=keyboard_markup,
                                   text='Темы:')


def set_right_answer_count_menu(update, bot_instance):
    # Формируем клавиатуру
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button(f'1', callback_data='@ac_1'),
         bot_instance.inline_keyboard_button(f'3', callback_data='@ac_3'),
         bot_instance.inline_keyboard_button(f'5', callback_data='@ac_5')],
        [bot_instance.inline_keyboard_button(f'7', callback_data='@ac_7'),
         bot_instance.inline_keyboard_button(f'10', callback_data='@ac_10'),
         bot_instance.inline_keyboard_button(f'15', callback_data='@ac_15')],
        [bot_instance.inline_keyboard_button(f'Назад', callback_data=f'{states.SETTINGS}'),
         bot_instance.inline_keyboard_button(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    # bot_instance.send_message(chat_id, f'Ваш результат: {result} из {data[4]}',
    #                           reply_markup=keyboard_markup)
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.send_message(chat_id, 'Количество правильных ответов:', reply_markup=keyboard_markup,
                              reply_to_message_id=message_id)


def set_session_words_count_menu(update, bot_instance):
    # Формируем клавиатуру
    keyboard_markup = bot_instance.inline_keyboard_markup([
        [bot_instance.inline_keyboard_button(f'1', callback_data='@wc_1'),
         bot_instance.inline_keyboard_button(f'3', callback_data='@wc_3'),
         bot_instance.inline_keyboard_button(f'5', callback_data='@wc_5')],
        [bot_instance.inline_keyboard_button(f'7', callback_data='@wc_7'),
         bot_instance.inline_keyboard_button(f'10', callback_data='@wc_10'),
         bot_instance.inline_keyboard_button(f'15', callback_data='@wc_15')],
        [bot_instance.inline_keyboard_button(f'Назад', callback_data=f'{states.SETTINGS}'),
         bot_instance.inline_keyboard_button(f'На главную', callback_data=f'{states.EXIT}')],
    ])
    chat_id = update['callback_query']['message']['chat']['id']
    message_id = update['callback_query']['message']['message_id']
    bot_instance.answer_callback_query(update['callback_query']['id'])
    bot_instance.send_message(chat_id, 'Количество вопросов в тесте:', reply_markup=keyboard_markup,
                              reply_to_message_id=message_id)


def set_theme(update, bot_instance):
    # Получаем или создаем пользователя
    user = get_user(update['callback_query']['message']['chat']['id'])

    # Изменяем настройки пользователя
    user.settings.theme_id = update['callback_query']['data'].split('_')[1]
    user.save()
    # Возвращаемся на главный экран
    start.restart(update, bot_instance)


def set_right_answer_count(update, bot_instance):
    # Получаем или создаем пользователя
    user = get_user(update['callback_query']['message']['chat']['id'])

    # Изменяем настройки пользователя
    user.settings.right_answer_count = update['callback_query']['data'].split('_')[1]
    user.save()
    # Возвращаемся на главный экран
    start.restart(update, bot_instance)


def set_session_words_count(update, bot_instance):
    # Получаем или создаем пользователя
    user = get_user(update['callback_query']['message']['chat']['id'])

    # Изменяем настройки пользователя
    user.settings.session_words_count = update['callback_query']['data'].split('_')[1]
    user.save()
    # Возвращаемся на главный экран
    start.restart(update, bot_instance)
