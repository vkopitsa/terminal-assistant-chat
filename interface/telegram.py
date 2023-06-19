from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import logging

from interface import Interface


class TelegramBot(Interface):
    app: Application

    def __init__(self, api_key, provider, user_access=""):
        self.api_key = api_key
        self.user_access = list(map(int, user_access.split(","))) if user_access != "" else []
        self.provider = provider

    async def process(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.message or not update.message.from_user:
            return

        if update.message.from_user.id not in self.user_access:
            await update.message.reply_text(f"forbidden: {update.message.from_user.username} [{update.message.from_user.id}]")
            return

        msg = self.provider.process_msg(update.message.text, update=update, context=context, uid=update.message.from_user.id)
        logging.info(f"sent: {msg}")
        if msg == "":
            msg = "The request was processed but had no response."
        if isinstance(msg, str) and len(msg) > 4096:
            msg = msg[:4096]
        await update.message.reply_text(msg)

    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.message or not update.message.from_user or not update.effective_message:
            return

        self.provider.add_history_message(reset=True, uid=update.message.from_user.id)
        await update.effective_message.reply_text("Context cleaned.")

    async def downloader(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.message or not update.message.from_user or update.message.from_user.id not in self.user_access:
            return

        document = update.message.document
        photo = update.message.photo

        if document:
            file = await context.bot.get_file(document)
            file_name = document.file_name

        if photo:
            file = await context.bot.get_file(photo[-1])
            file_name = f"{file.file_unique_id}.png"

        await file.download_to_drive(f"files/{file_name}")

        self.provider.add_history_message(msgs=[{
            "role": "user",
            "content": f"uploaded file: files/{file_name}"
        }], uid=update.message.from_user.id)

    def run(self):
        self.app = ApplicationBuilder().token(self.api_key).build()
        self.app.add_handler(MessageHandler(((~filters.COMMAND) & (~filters.ATTACHMENT)), self.process))
        self.app.add_handler(MessageHandler(filters.ATTACHMENT, self.downloader))
        self.app.add_handler(CommandHandler("clear", self.clear))
        self.app.run_polling()
