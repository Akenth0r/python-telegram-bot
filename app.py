from flask import Flask, Response, request
from bot import LanguageLearningBot
import os
import sqlalchemy
from fpdf import FPDF
# https://api.telegram.org/bot1623674677:AAFNHd1PgUbzKH3YW7nUoUGXKzEePGGq3tY/setWebhook?url=https://5ac3d6c47f25.ngrok.io
from db import User, Session, get_user_remembered_words, Theme, ThemeWord

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
    response = bot.set_webhook(f'{URL}/{TOKEN}')
    return Response(response)


@app.route("/sendmessage")
def send_message():
    bot.send_message(request.args.get('to'), request.args.get('message'))

    return Response(status=200)

@app.route('/broadcast')
def broadcast():
    session = Session()
    users = session.query(User).all()
    for user in users:
        bot.send_message(user.id, request.args.get('message'))

    return Response(request.args.get('message'))

@app.route('/')
def index():
    session = Session()
    users = session.query(User).all()
    output = "<html><head></head><body>"
    for user in users:
        output += f'user: {user.id} <br>'
        user_remembered_words = get_user_remembered_words(user)
        for i in range(len(user.statistics.remembered_words)):
            output += f'    {user_remembered_words[i].original} - {user.statistics.remembered_words[i].updated_at} <br>'
        output += "<br>"
    output += "</body></html>"
    return output

def get_user_statistics_html(user: User):
    output = ""
    user_remembered_words = get_user_remembered_words(user)
    for i in range(len(user.statistics.remembered_words)):
        output += f'\t{user_remembered_words[i].original} - {user.statistics.remembered_words[i].updated_at} \n'
    output += "\n"

    return output

@app.route('/addTheme')
def add_new_theme():
    session = Session()
    theme_id = request.args.get('theme_id')
    if not theme_id:
        return 'theme_id needed'

    theme = session.get(Theme, theme_id)
    if not theme:
        theme = Theme()
        theme.id = theme_id
        session.add(theme)
        session.commit()
        return f'Theme was added successfully: {theme_id}'
    return f'Theme already exists: {theme_id}'

@app.route('addWord')
def add_word_to_theme():
    session = Session()
    theme_id = request.args.get('theme_id')
    original = request.args.get('original')
    translation = request.args.get('translation')
    example = request.args.get('example')
    if not (theme_id or original or translation or example):
        return "not enough arguments"
    word = session.query(ThemeWord).filter((ThemeWord.theme_id == theme_id) & (ThemeWord.original == original) & (ThemeWord.translation == translation)).one_or_none()
    if not word:
        word = ThemeWord()
        word.theme_id = theme_id
        word.original = original
        word.translation = translation
        word.example = example
        session.add(word)
        session.commit()
        return f'Word added: {original}'

    return f'Word already exists: {original}'