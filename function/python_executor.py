import logging
import sys
from io import StringIO

from typing import Any, AnyStr

from .function import Function


class PythonExecutor(Function):
    specification = {
        "name": "execute_python_code",
        "description": "Execute Python code and return the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to execute.",
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
        logging.warning(f">>> {code}")

        # redirect stdout to a string
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        try:
            exec(code)
        except Exception as e:
            logging.error(e)
        finally:
            # reset stdout
            sys.stdout = old_stdout

        return redirected_output.getvalue()
