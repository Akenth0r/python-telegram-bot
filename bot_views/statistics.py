from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext


def get_statistics(update: Update, context: CallbackContext):
    update.message.reply_text('Вот статистика ХЫ')
    return ConversationHandler.END