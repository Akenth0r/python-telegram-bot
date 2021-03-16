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
    if not user.load_or_init(str(update.callback_query.message.chat_id)):
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
    wc = int(user.settings.session_words_count)
    print(f'Количество вопросов: {wc}')
    #words_for_test: List[ThemeWord] = all_words[0:wc]
    current_word = all_words[number_of_question]

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
                              callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[0].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'{words_to_show[1].translation}',
                              callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[1].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'{words_to_show[2].translation}',
                              callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[2].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'{words_to_show[3].translation}',
                              callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[3].original}_{wc}_{theme_id}_{0}')],
        [InlineKeyboardButton(f'Показать пример', callback_data='@example'),
            InlineKeyboardButton(f'Завершить тест', callback_data='@exit')],
    ])

    update.callback_query.message.reply_text(
        f'Вопрос {number_of_question + 1}\nВыберите перевод слова: {current_word.original}',
        reply_markup=keyboard_markup)
    return states.TEST


def test(update: Update, context: CallbackContext):
    # update.callback_query.data
    print('Продолжаем тест')
    raw_data = update.callback_query.data
    data = raw_data.split('_')
    result = int(data[6])
    number_of_question = int(data[1]) + 1

    user = User()
    user.load_or_init(str(update.callback_query.message.chat_id))
    word_dict = user.statistics.remembered_words_list
    word = data[2]

    if data[2] == data[3]:
        # + 1 балл в статистику
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict.setdefault(word, 1)
        user.save()

        # и в историю
        result += 1
        pass

    else:
        # обнуление в статистике
        if word in word_dict:
            word_dict[word] = 0
        else:
            word_dict.setdefault(word, 0)
        user.save()
        pass

    if number_of_question >= int(data[4]):
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'Окей', callback_data='@exit')]])
        update.callback_query.message.reply_text( f'Ваш результат: {result} из {data[4]}', reply_markup=keyboard_markup)
    else:
        # Получаем текущую тему
        theme_id = data[5]
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
                                  callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[0].original}_{data[4]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'{words_to_show[1].translation}',
                                  callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[1].original}_{data[4]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'{words_to_show[2].translation}',
                                  callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[2].original}_{data[4]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'{words_to_show[3].translation}',
                                  callback_data=f'@_{number_of_question}_{current_word.original}_{words_to_show[3].original}_{data[4]}_{theme_id}_{result}')],
            [InlineKeyboardButton(f'Показать пример', callback_data='@example'),
             InlineKeyboardButton(f'Завершить тест', callback_data='@exit')],
        ])

        update.callback_query.message.reply_text(
            f'Вопрос {number_of_question + 1}\nВыберите перевод слова: {current_word.original}',
            reply_markup=keyboard_markup)
    return states.TEST


def test_end(update: Update, context: CallbackContext):
    pass
