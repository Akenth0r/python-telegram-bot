import requests
import json


class Bot:
    def __init__(self, token, debug=False):
        self.token = token

    def _telegram_method(self, method_name, json_data):
        url = f"https://api.telegram.org/bot{self.token}/{method_name}"
        r = requests.post(url, data=json_data)
        # if self.debug:
        #    print(r.text)
        return r

    def send_message(self, chat_id, text, keyboard_array=None, reply_to_message_id=None):
        data = {"chat_id": chat_id, "text": text}
        if keyboard_array is not None:
            data["reply_markup"] = self._reply_keyboard(keyboard_array)
        if reply_to_message_id is not None:
            data["reply_to_message_id"] = reply_to_message_id
        self._telegram_method("sendMessage", data)  # response: Response =

    def _reply_keyboard(self, keyboard_array):
        reply_markup = {"keyboard": keyboard_array, "resize_keyboard": True, "one_time_keyboard": True}
        return json.dumps(reply_markup)
