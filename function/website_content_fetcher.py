import requests
import logging
from bs4 import BeautifulSoup
from typing import Any, AnyStr

from .function import Function


class WebsiteContentFetcher(Function):
    specification = {
        "name": "get_website_content",
        "description": "Gets the content of a website",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the website",
                },
                "continue": {
                    "type": "string",
                    "enum": ["true", "false"],
                    "description": "The boolean flag that determines whether to process output from the function. If set to true, the function's output will be processed. If set to false, the function's output will not be processed. ",
                },
            },
            "required": ["url", "continue"],
        },
    }

    def get_name(self) -> AnyStr:
        return self.specification.get("name", "")

    def func(self, data, **kwargs) -> Any:
        url = data if isinstance(data, str) else data.get("url")
        logging.warning(f"URI# {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
