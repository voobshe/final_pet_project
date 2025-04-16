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
        self.application.add_handler(CommandHandler("clear", LisaBot.clear_data))
        self.application.add_handler(CommandHandler("calc", LisaBot.calculate))
        self.application.add_handler(MessageHandler(filters.PHOTO, LisaBot.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, LisaBot.handle_text))
        self.application.bot_data = self

        self.photo_data = list()
        self.user_data = dict()
        self.katusha = katusha_part
        


    async def start(update: Update, context:CallbackContext)->None:
        """
        This method asks the user to send the price tag of the product.
        """

        user_id = context._user_id
        reply = ''
        mb_photo_data = self.user_data.get(user_id)
        if mb_photo_data == None:
            self.user_data[user_id] = list()
            reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

        #self.logger.info(f"User {update.effective_user.full_name} started the bot")
        await update.message.reply_text('Отправь фотографию ценников')


    async def clear_data(update: Update, context:CallbackContext)->None:
        """
        this method clear photo data
        """
        self = context.bot_data

        user_id = context._user_id
        reply = ''
        mb_photo_data = self.user_data.get(user_id)
        if mb_photo_data == None:
            self.user_data[user_id] = list()
            reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

        reply = f"количество записей в списке: {len(self.user_data[user_id])} \n"
        reply += "список очищен"

        self.user_data[user_id].clear()
        #self.logger.info(f"User {update.effective_user.full_name} started the bot")
        await update.message.reply_text(reply)

    async def calculate(update: Update, context:CallbackContext)->None:
        """
        this method calculate optimal price
        """
        self = context.bot_data

        user_id = context._user_id
        reply = ''
        mb_photo_data = self.user_data.get(user_id)
        if mb_photo_data == None:
            self.user_data[user_id] = list()
            reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

        reply = f"список содержал {len(self.user_data[user_id])} записи\n"
        # pass user_data[user_id] to katusha.photo_handler
        photos = self.user_data[user_id]
        reply += "рассчеты проведены\n"
        reply += "список url фотографий: \n "
        for photo_url in photos:
            reply += f"{photo_url}\n"
        self.user_data[user_id].clear()
        #self.logger.info(f"User {update.effective_user.full_name} started the bot")
        await update.message.reply_text(reply)


    async def handle_photo(update: Update, context:CallbackContext):
        """
        This method accepts photo.
        """
        self = context.bot_data
        user_id = context._user_id
        reply = ''
        mb_photo_data = self.user_data.get(user_id)
        if mb_photo_data == None:
            self.user_data[user_id] = list()
            reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

        #lisa = context.bot_data
        photo = update.message.photo[-1]

        file = await photo.get_file()
        photo_url = file.file_path
        #file = file.download_file(file_path)
        self.user_data[user_id].append(photo_url)
        pd_len = len(self.user_data[user_id])
        
        reply += f'Добавлена фотография для сравнения.\n Всего для сравнения {pd_len} фотографий'        
        #self.logger.info(f"Фото получено от: {update.effective_user.full_name}")
        await update.message.reply_text(reply)
        

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