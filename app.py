from flask import Flask, Response, request
from telegram.ext import Updater
import telegram
from bot import LanguageLearningBot
import os
import sqlalchemy

# https://api.telegram.org/bot1623674677:AAFNHd1PgUbzKH3YW7nUoUGXKzEePGGq3tY/setWebhook?url=https://5ac3d6c47f25.ngrok.io
from db import session, User

TOKEN = os.getenv('TOKEN')  # '1623674677:AAGhGrT-8icuj1niyMnD5fntn2MmsCH7vB4'  # AAFNHd1PgUbzKH3YW7nUoUGXKzWePGGGq3tY
URL = os.getenv('URL')
# Хитро получаем абсолютный путь (для локального сервера)
DEBUG = False

app = Flask(__name__)
bot = LanguageLearningBot(TOKEN)


@app.route(f"/{TOKEN}", methods=["GET", "POST"])
def receive_update():
    bot.handle_update(request.json)

    return Response(status=200)


@app.route("/setWebhook")
def set_webhook():
    bot.updater.bot.set_webhook(
        f'{URL}/{TOKEN}',
        max_connections=100,
    )
    return 'ok'


@app.route("/sendmessage")
def set_message():
    bot.updater.bot.send_message(request.args.get('to'), request.args.get('message'))

    return Response(status=200)

@app.route('/broadcast')
def broadcast():
    users = session.query(User).all()
    for user in users:
        bot.updater.bot.send_message(user.id, request.args.get('message'))

    return Response(request.args.get('message'))

@app.route('/get_file')
def get_file():
    file = bot.updater.bot.get_file(request.args.get('file_id'))
    file.download(request.args.get('file_id'))
    return 'ok'