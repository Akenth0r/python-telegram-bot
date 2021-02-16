import json

import requests

METHOD_SEND_MESSAGE = 'sendMessage'


def reply_keyboard(keyboard_array):
    reply_markup = {"keyboard": keyboard_array, "resize_keyboard": True, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def telegram_method(method_name, json_data, url):
    method_url = f"{url}/{method_name}"
    r = requests.post(method_url, data=json_data)

    return r
