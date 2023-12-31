from typing import Dict, List
import logging
import json
import openai
from utils import is_json


class OpenAIChat:
    init_settings = [
        {"role": "system", "content": "You are an assistant."},
        {"role": "system", "content": "You can execute Python code, Bash, and Ubuntu terminal commands as root."},
        {"role": "system", "content": "You can install tools or Python modules."},
        {"role": "system", "content": "Avoid actions harmful to the operating system."},
        {"role": "system", "content": "You can search (using Google) with the bash command: \"ddgr -n 3 [search keywords]\""},
        {"role": "system", "content": "Retrieve weather data from: https://api.open-meteo.com/v1/forecast?latitude=:latitude&longitude=:longitude&temperature_unit=celsius&current_weather=true"},
        {"role": "system", "content": "Fetch public holidays: https://date.nager.at/api/v3/publicholidays/{year}/{country_code}"},
    ]

    _chat_history: Dict[int, List] = {}

    def __init__(self, model, funcs=[]):
        self.model = model
        self.funcs = funcs

    def add_history_message(self, msgs=[], uid=0, reset=False):
        if uid not in self._chat_history or reset:
            self._chat_history[uid] = []

        if len(msgs) != 0:
            self._chat_history[uid].extend(msgs)

        if len(self._chat_history[uid]) > 10:
            self._chat_history[uid] = self._chat_history[uid][-9:]

    def get_history_message(self, uid=0):
        return self._chat_history[uid]

    def send_to_openai(self, messages=[], uid=0):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                functions=list(map(lambda f: f.specification, self.funcs)),
                function_call="auto",
            )

            return response
        except Exception as e:
            logging.error(e)
            if "maximum context length" in str(e):
                self.add_history_message(reset=True, uid=uid)

            return str(e)

    def build_messages(self, msg, uid=0):
        messages = self.init_settings[:]

        if msg != "":
            self.add_history_message(msgs=[{"role": "user", "content": msg}], uid=uid)

        messages.extend(self.get_history_message(uid))

        return messages

    def process_msg(self, msg, attempts=0, uid=0, **kwargs):
        response = self.send_to_openai(messages=self.build_messages(msg, uid=uid), uid=uid)
        if isinstance(response, str):
            return response

        message = response["choices"][0]["message"]
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            _data = message["function_call"]["arguments"]
            logging.warning(function_name)
            logging.warning(_data)
            data = {}
            try:
                data = json.loads(_data) if is_json(_data) else _data

                for func in self.funcs:
                    if func.get_name() == function_name:
                        function_response = func.func(
                            data=data,
                            uid=uid,
                            **kwargs
                        )
            except Exception as e:
                logging.debug(_data)
                logging.error(e)
                function_response = str(e)

            logging.warning(f"\n\n{function_response}")

            self.add_history_message(
                msgs=[{
                    "role": "function",
                    "name": function_name,
                    "content": str(function_response),
                }],
                uid=uid
            )

            logging.warning(attempts)
            if isinstance(data, dict) and data.get("continue", "false") == "true" and attempts < 5:
                logging.info("Thinking...")
                return self.process_msg("", uid=uid, attempts=attempts + 1, **kwargs)
            return function_response
        else:
            self.add_history_message(msgs=[message], uid=uid)
            return message.content
