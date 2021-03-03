from typing import List

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

import states
import random
from bot_models.theme import Theme, ThemeWord


# Возможно нужно создать класс чтобы у методы могли менять счетчик и тему
number_of_questions = 3
question_counter = 0
words_for_test = []
theme_name = 'animals'

def test_begin(update: Update, context: CallbackContext):
    #update.callback_query.message.reply_text("Начинаем наш тест...")

    # Вот тут мы подгружаем слова по теме и считаем число правильных ответов
    current_theme: Theme = Theme()
    current_theme.load(theme_name)

    all_words: List[ThemeWord] = current_theme.words
    random.shuffle(all_words)

    # Нужно сохранить или вести счетчик по number_of_questions
    words_for_test: List[ThemeWord] = all_words[0:number_of_questions]
    question_counter = number_of_questions - 1

    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'{all_words[0].translation}', callback_data=str(states.TEST))],
        [InlineKeyboardButton(f'{all_words[1].translation}', callback_data=str(states.TEST))],
        [InlineKeyboardButton(f'{all_words[2].translation}', callback_data=str(states.TEST))],
        [InlineKeyboardButton(f'{all_words[3].translation}', callback_data=str(states.TEST))],
    ])

    update.callback_query.message.reply_text(f'Выберите перевод слова: {words_for_test[question_counter].original}', reply_markup=keyboard_markup)
    return states.TEST


def test(update: Update, context: CallbackContext):
    pass


def test_end(update: Update, context: CallbackContext):
    pass
