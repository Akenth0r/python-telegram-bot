from flask import Flask, request, Response
from bot import Bot
from datetime import datetime, timedelta

# Made by catinapoke with Akenth0r

TOKEN = '1623674677:AAFNHd1PgUbzKH3YW7nUoUGXKzEePGGq3tY'  # AAFNHd1PgUbzKH3YW7nUoUGXKzWePGGGq3tY
DEBUG = False

app = Flask(__name__)
bot = Bot(TOKEN)


def start_handler(message: dict):
    bot.send_message(message['chat']['id'], 'Hello to you in back!')


bot.add_handler('hello', start_handler)


def handle_message(message: dict):
    # chat_id = request.json["message"]["chat"]["id"]
    # text = request.json["message"]["text"]
    # bot.send_message(chat_id, f"I got message \"{text}\"", [["Адин"], ["Два", "Три"]],
    #                  reply_to_message_id=request.json["message"]["message_id"])
    # if DEBUG:
    #     for var in request.json:
    #         print(f'{var}; {request.json[var]}')
    bot.handle_message(message['message'])


def check_timestamp(timestamp):
    timestamp = request.json["message"]["date"]
    dt_object = datetime.fromtimestamp(timestamp)
    return (datetime.now() - dt_object) > timedelta(minutes=5)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST" and not check_timestamp(request.json["message"]["date"]):
        handle_message(request.json)

    return Response('{"ok": true}', status=200, mimetype='application/json')

# https://flask-aiohttp.readthedocs.io/en/latest/
