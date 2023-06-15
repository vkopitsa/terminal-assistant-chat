import logging
import sys
from io import StringIO

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
        return self.specification.get("name")

    def func(self, data) -> Any:
        code = data if isinstance(data, str) else data.get("code")
        logging.warning(f">>> {code}")

        # Redirect stdout to a string
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        try:
            exec(code)
        except Exception as e:
            logging.error(e)
        finally:
            # Reset stdout
            sys.stdout = old_stdout

        return redirected_output.getvalue()
