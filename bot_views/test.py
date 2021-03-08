from typing import List

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

import states
import random
from bot_models.theme import Theme, ThemeWord

from bot_models.user import User, UserSettings, UserStatistics

question_counter = 0
words_for_test = []


# theme_name = 'animals'

def test_begin(update: Update, context: CallbackContext):
    # Кандидат для метода бота get_user()
    user = User()
    print(f'Чат id{update.callback_query.message.chat_id}')
    if not user.load(str(update.callback_query.message.chat_id)):
        user.user_id = update.callback_query.message.chat_id
        user.settings = UserSettings()
        user.statistics = UserStatistics()
        user.save()
    print('Получили юзера')

    # Вот тут мы подгружаем слова по теме и считаем число правильных ответов
    theme_id = user.settings.theme_id
    current_theme: Theme = Theme()
    current_theme.load(theme_id)
    print(f'Получили тему {theme_id}')

    # Получаем все слова из темы
    all_words: List[ThemeWord] = current_theme.words
    random.shuffle(all_words)
    print(f'Получили слова: {len(all_words)}')

    # Номер вопроса
    number_of_question = 0

    # Нужно сохранить или вести счетчик по number_of_questions
    wc = user.settings.session_words_count
    words_for_test: List[ThemeWord] = all_words[0:wc]
    current_word = words_for_test[number_of_question]

    # Формируем слова для вопроса
    random.shuffle(all_words)
    words_to_show = all_words[0:3]
    words_to_show.append(current_word)
    print(f'Должно быть 4 слова: {len(words_to_show)}')
    random.shuffle(words_to_show)
    # {words_for_test}_
    # f'{number_of_question}_{current_word}_{words_to_show[0]}'
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'{words_to_show[0].translation}',
                              callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[0].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'{words_to_show[1].translation}',
                              callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[1].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'{words_to_show[2].translation}',
                              callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[2].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'{words_to_show[3].translation}',
                              callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[3].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'Показать пример', callback_data='@example'),
            InlineKeyboardButton(f'Завершить тест', callback_data='@exit')],
    ])

    update.callback_query.message.reply_text(
        f'Вопрос {number_of_question + 1}\nВыберите перевод слова: {words_for_test[number_of_question].original}',
        reply_markup=keyboard_markup)
    return states.TEST


def test(update: Update, context: CallbackContext):
    # update.callback_query.data
    print('Продолжаем тест')
    raw_data = update.callback_query.data
    data = raw_data.split('_')
    result = int(data[5])
    number_of_question = int(data[0]) + 1
    if data[1] == data[2]:
        # + 1 балл в статистику
        result += 1
        pass

    else:
        # обнуление в статистике
        pass

    if number_of_question >= int(data[3]):
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'Окей', callback_data='@exit')]])
        update.callback_query.message.reply_text( f'Ваш результат: {result} из {data[3]}', reply_markup=keyboard_markup)
    else:
        # Получаем текущую тему
        theme_id = data[4]
        current_theme: Theme = Theme()
        current_theme.load(theme_id)
        print(f'Получили тему {theme_id}')

        # Получаем все слова из темы
        all_words: List[ThemeWord] = current_theme.words
        random.shuffle(all_words)

        # Выбираем текущее слово и слова для показа
        current_word = all_words[0]
        words_to_show = all_words[1:4]
        words_to_show.append(current_word)
        print(f'Должно быть 4 слова: {len(words_to_show)}')
        random.shuffle(words_to_show)

        # Формируем клавиатуру
        keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f'{words_to_show[0].translation}',
                                  callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[0].original}_{data[3]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'{words_to_show[1].translation}',
                                  callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[1].original}_{data[3]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'{words_to_show[2].translation}',
                                  callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[2].original}_{data[3]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'{words_to_show[3].translation}',
                                  callback_data=f'{number_of_question}_{current_word.original}_{words_to_show[3].original}_{data[3]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'Показать пример', callback_data='@example'),
             InlineKeyboardButton(f'Завершить тест', callback_data='@exit')],
        ])

    update.callback_query.message.reply_text(
        f'Вопрос {number_of_question + 1}\nВыберите перевод слова: {current_word.original}',
        reply_markup=keyboard_markup)
    return states.TEST


def test_end(update: Update, context: CallbackContext):
    pass
