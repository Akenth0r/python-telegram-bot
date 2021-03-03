from typing import List

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

import states
import random
from bot_models.theme import Theme, ThemeWord

# class Test:
#     def __init__(self, theme_name = 'animals', question_number = 3):
#         self.words_for_test = []
#         self.theme_name = theme_name
#         self.question_counter = question_number
# # Возможно нужно создать класс чтобы у методы могли менять счетчик и тему
from bot_models.user import User, UserSettings, UserStatistics

number_of_questions = 3
question_counter = 0
words_for_test = []
#theme_name = 'animals'

def test_begin(update: Update, context: CallbackContext):
    # Кандидат для метода бота get_user()
    user = User()
    if not user.load(str(update.message.chat_id)):
        user.user_id = update.message.chat_id
        user.settings = UserSettings()
        user.statistics = UserStatistics()
        user.save()

    # Вот тут мы подгружаем слова по теме и считаем число правильных ответов
    current_theme: Theme = Theme()
    current_theme.load(user.settings.theme_id)

    # Получаем все слова из темы
    all_words: List[ThemeWord] = current_theme.words
    random.shuffle(all_words)

    # Нужно сохранить или вести счетчик по number_of_questions
    words_for_test: List[ThemeWord] = all_words[0:user.settings.session_words_count]
    current_word = words_for_test[number_of_questions]

    question_counter = number_of_questions - 1


    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'{all_words[0].translation}', callback_data=f'test_{number_of_questions}__')], # callback → 'question_n_1'
        [InlineKeyboardButton(f'{all_words[1].translation}', callback_data=f'test_{number_of_questions}__')], # callback → 'question_n_2'
        [InlineKeyboardButton(f'{all_words[2].translation}', callback_data=f'test_{number_of_questions}__')], # callback → 'question_n_3'
        [InlineKeyboardButton(f'{all_words[3].translation}', callback_data=f'test_{number_of_questions}__')], # callback → 'question_n_4'
    ])

    update.callback_query.message.reply_text(f'Выберите перевод слова: {words_for_test[question_counter].original}', reply_markup=keyboard_markup)
    return states.TEST


def test(update: Update, context: CallbackContext):
    pass


def test_end(update: Update, context: CallbackContext):
    pass
