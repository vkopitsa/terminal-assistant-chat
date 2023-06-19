import asyncio

from typing import Any, AnyStr

from .function import Function


class FileSender(Function):
    specification = {
        "name": "send_file",
        "description": "Sends a file to a Telegram chat",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The file path to send"
                },
            },
            "required": ["filepath"],
        },
    }

    def get_name(self) -> AnyStr:
        return self.specification.get("name", "")

    def func(self, data, **kwargs) -> Any:
        update = kwargs.get("update")
        context = kwargs.get("context")

        if not update or not context:
            return ""

        chat_id = update.message.chat_id

        filepath = data if isinstance(data, str) else data.get("filepath")

        document = open(filepath, 'rb')
        asyncio.create_task(context.bot.send_document(chat_id, document))

        return "Done!"
