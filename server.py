#!/bin/python3

from bot_key import BOT_KEY
import asyncio
import logging
from gemini_ocr import Katusha, Product
from wolf_bot_key import wolf_api_key

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
from bot import start, clear_data, calculate, handle_photo, handle_text, best_product_command

def main():
    """
    TODO: add description
    """
    global BOT_KEY
    bot = ApplicationBuilder().token(BOT_KEY).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("clear", clear_data))
    bot.add_handler(CommandHandler("calc", calculate))
    bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    bot.add_handler(CommandHandler("best", best_product_command))
    # Bot ctor is long op, so it's should be done once at session start
    # price tracker will be stored in foxbot data
    price_tracker = Katusha(key=wolf_api_key)
    bot.bot_data = {"pt":price_tracker}

    photo_data = list()
    user_data = dict()
    # katusha = katusha_part
    bot.run_polling()
    return 0

if __name__ == '__main__':
    ret = main()
    exit(ret)