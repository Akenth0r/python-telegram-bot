from telegram import Update
from telegram.ext import CallbackContext


def end(update: Update, context: CallbackContext):
    update.message.reply_text('А ну давай')