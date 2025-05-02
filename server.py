#!/bin/python3

from bot_key import BOT_KEY
import asyncio
import logging

# you should generate bot_key.py with BOT_KEY = "your telegram bot key"
# and put it into gitignore

from sqlalchemy.orm import sessionmaker

from telegram.constants import ParseMode


from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
    CallbackContext
)
from bot import start, clear_data, calculate, handle_photo, handle_text

def main():
    """
    TODO: add description
    """
    global BOT_KEY
    #TODO добавить катюшин обработчик изображений
    print(BOT_KEY)
    bot = ApplicationBuilder().token(BOT_KEY).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("clear", clear_data))
    bot.add_handler(CommandHandler("calc", calculate))
    bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    photo_data = list()
    user_data = dict()
    # katusha = katusha_part
    bot.run_polling()
    return 0

if __name__ == '__main__':
    ret = main()
    exit(ret)