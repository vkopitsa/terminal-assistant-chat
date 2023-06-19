import logging
from typing import Any, AnyStr

from .function import Function


class ExpressionExecutor(Function):
    specification = {
        "name": "execute_python_expression",
        "description": "Execute Python expression and return the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python expression to execute.",
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
        logging.warning(f"= {code}\n")

        try:
            output = eval(code)
            return output
        except Exception as e:
            logging.error(e)
            return str(e)
