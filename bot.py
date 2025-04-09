import asyncio
import logging

# you should generate bot_key.py with BOT_KEY = "your telegram bot key"
# and put it into gitignore
from bot_key import BOT_KEY

from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
    CallbackContext,
)

class LisaBot:
    """
    This class asks the user to send a photo of the product price tag,
    accepts a photo of the product price tag, and processes it.

    Attributes
    ----------
    application
        telegram bot app

    Methods
    -------
    run()
        Start pooling routine
    """
    def __init__(self, bot_key, katusha_part):
        self.application = Application.builder().token(BOT_KEY).build()

        self.application.add_handler(CommandHandler("start", LisaBot.start))
        self.application.add_handler(MessageHandler(filters.PHOTO, LisaBot.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, LisaBot.handle_text))
        self.application.bot_data = self


    async def start(update: Update, context:CallbackContext)->None:
        """
        This method asks the user to send the price tag of the product.
        """
        #self.logger.info(f"User {update.effective_user.full_name} started the bot")
        await update.message.reply_text('Отправь фотографию ценника.')

    async def handle_photo(update: Update, context:CallbackContext):
        """
        This method accepts photo.
        """
        #lisa = context.bot_data
        photo = update.message.photo[-1]
        file = await photo.get_file()
        #file = file.download_file(file_path)
        await file.download_to_drive("testfile.jpg")
        #self.logger.info(f"Фото получено от: {update.effective_user.full_name}")
        await update.message.reply_text('Я обрабатываю фотографию ценника')

    async def handle_text(update: Update, context:CallbackContext):
        """
        This method asks the user to send a photo of the product price tag, if the user sent text instead of a photo.
        """
        #self.logger.info(f"Текст получен от: {update.effective_user.full_name}: {update.message.text}")
        await update.message.reply_text('Пожалуйста, отправьте именно фотографию ценника.')
       
    def run(self):
        """
        This method starts the bot.
        """
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)