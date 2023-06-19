import logging
import subprocess
import os
from typing import Any, AnyStr

from .function import Function


class BashExecutor(Function):
    specification = {
        "name": "execute_bash_code",
        "description": "Execute bash code or terminal command and return the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The bash code or terminal command to execute.",
                },
                "continue": {
                    "type": "string",
                    "enum": ["true", "false"],
                    "description": "The boolean flag that determines whether to process output from the function. If set to true, the function's output will be processed. If set to false, the function's output will not be processed. ",
                },
            },
            "required": ["code", "continue"],
        },
    }

    def get_name(self) -> AnyStr:
        return self.specification.get("name", "")

    def func(self, data, **kwargs) -> Any:
        code = data if isinstance(data, str) else data.get("code")
        logging.warning(f"# {code}")
        try:
            if "files" not in os.getcwd():
                os.chdir("files/")
            process = subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
            if process.stderr:
                return process.stderr
            return process.stdout if process.stdout else "Done!"
        except Exception as e:
            logging.debug(data)
            logging.error(e)
            return str(e)
