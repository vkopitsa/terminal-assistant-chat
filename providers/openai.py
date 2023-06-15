import logging
import json
import openai
from utils import is_json


class OpenAIChat:
    init_settings = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": "You have a working directory: files/*"},
        {"role": "system", "content": "You must remove any extraneous information that is not essential to your prompt or question or answer. Be concise and focus on the key points."},
        {"role": "system", "content": "You can execute python code (use print function to show result), expression, bash code, or a terminal command on Ubuntu (how root user, not use sudo)"},
        {"role": "system", "content": "You can get the content of a website or URI"},
        {"role": "system", "content": "You can install missing python module."},
        {"role": "system", "content": "You can not do things that are dangerous to the OS."},
        {"role": "system", "content": "You can send a message to admin"},
        {"role": "system", "content": "You can search (using Google) with the bash command: \"ddgr --json -n 3 [search keywords]\""},
        {"role": "system", "content": "You can process output from any actions. For that, you can use a 'continue' parameter. But only 3 consecutive attempts"},
    ]

    chat_history = []

    def __init__(self, funcs=[]):
        self.funcs = funcs

    def send_to_openai(self, messages=[]):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                # model="gpt-4-0613",
                messages=messages,
                functions=list(map(lambda f: f.specification, self.funcs)),
                function_call="auto",
            )

            return response
        except Exception as e:
            logging.error(e)
            if "maximum context length" in str(e):
                self.chat_history = self.init_settings[:]

            return str(e)

    def build_messages(self, msg):
        messages = self.init_settings[:]

        if msg != "":
            self.chat_history.append({"role": "user", "content": msg})

        if len(self.chat_history) > 10:
            self.chat_history.pop(0)

        messages.extend(self.chat_history)

        return messages

    def process_msg(self, msg, attempts=0, update=None, context=None):
        response = self.send_to_openai(messages=self.build_messages(msg))
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
                # if is_json(_data):
                data = json.loads(_data) if is_json(_data) else _data

                for func in self.funcs:
                    if func.get_name() == function_name:
                        function_response = func.func(data=data)
            except Exception as e:
                logging.debug(_data)
                logging.error(e)
                function_response = str(e)

            logging.warning(f"\n\n{function_response}")

            self.chat_history.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })

            logging.warning(attempts)
            if isinstance(data, dict) and data.get("continue", "false") == "true" and attempts < 5:
                logging.info("Thinking...")
                return self.process_msg("", attempts=attempts + 1, update=update, context=context)
            return function_response
        else:
            self.chat_history.append(message)
            return message.content
