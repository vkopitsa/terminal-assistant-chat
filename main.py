import sys
import os
import logging
from typing import List

from function import Function, BashExecutor, ExpressionExecutor, FileSender, MessageSender, PythonExecutor, WebsiteContentFetcher
from providers import OpenAIChat
from interface import TelegramBot, Terminal


TG_API_KEY = os.getenv("TG_API_KEY")
TG_ADMIN_CHAT_ID = os.getenv("TG_ADMIN_CHAT_ID")
TG_USER_ACCESS = os.getenv("TG_USER_ACCESS", "")


funcs: List[Function] = [
    BashExecutor(),
    ExpressionExecutor(),
    FileSender(),
    MessageSender(TG_API_KEY, TG_ADMIN_CHAT_ID),
    PythonExecutor(),
    WebsiteContentFetcher(),
]

oa = OpenAIChat(funcs=funcs)

if __name__ == "__main__":
    if "telegram" in sys.argv:
        TelegramBot(api_key=TG_API_KEY, provider=oa, user_access=TG_USER_ACCESS).run()
    else:
        logging.basicConfig(level=logging.CRITICAL)

        Terminal(provider=oa).run()
