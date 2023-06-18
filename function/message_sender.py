import requests
from typing import Any, AnyStr

from .function import Function


class MessageSender(Function):
    specification = {
        "name": "send_message_to_admin",
        "description": "Sends a message to a admin",
        "parameters": {
            "type": "object",
            "properties": {
                "msg": {
                    "type": "string",
                    "description": "The text of the message"
                },
            },
            "required": ["msg"],
        },
    }

    def __init__(self, tg_api_key, tg_admin_chat_id):
        self.tg_api_key = tg_api_key
        self.tg_admin_chat_id = tg_admin_chat_id

    def get_name(self) -> AnyStr:
        return self.specification.get("name")

    def func(self, data, **kwargs) -> Any:
        msg = data if isinstance(data, str) else data.get("msg")
        url = f"https://api.telegram.org/bot{self.tg_api_key}/sendMessage"
        data = {
            "parse_mode": "Markdown",
            "disable_notification": "true",
            "chat_id": self.tg_admin_chat_id,
            "text": msg
        }
        response = requests.post(url, data=data)
        return "Sent!" if response.status_code == 200 else "Got error!"
