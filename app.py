from flask import Flask, Response, request
from telegram.ext import Updater
import telegram
from bot import LanguageLearningBot
import os

# https://api.telegram.org/bot1623674677:AAFNHd1PgUbzKH3YW7nUoUGXKzEePGGq3tY/setWebhook?url=https://5ac3d6c47f25.ngrok.io

TOKEN = '1623674677:AAF6i_aZ9BCio7cVOpQUALDTmeEGeUF1hBE'  # AAFNHd1PgUbzKH3YW7nUoUGXKzWePGGGq3tY
URL = 'https://a436ee2caa1a.ngrok.io'
# Хитро получаем абсолютный путь (для локального сервера)
DEBUG = False

app = Flask(__name__)
bot = LanguageLearningBot(TOKEN)


@app.route(f"/{TOKEN}", methods=["GET", "POST"])
def receive_update():
    bot.handle_update(request.json)

    return {'ok': True}


@app.route("/setWebhook")
def set_webhook():
    bot.updater.bot.set_webhook(
        f'{URL}/{TOKEN}'
    )
    return 'ok'
