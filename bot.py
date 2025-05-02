import asyncio
import logging

from sqlalchemy import select

# you should generate bot_key.py with BOT_KEY = "your telegram bot key"
# and put it into gitignore
from models import User, ProcessingResult
from db import db_session

from telegram import (
    Update,
)
from telegram.constants import ParseMode

from telegram.ext import (
    CallbackContext
)

user_data = {}


async def start(update: Update, context:CallbackContext)->None:
    """
    This method asks the user to send the price tag of the product.
    """

    user_id = context._user_id
    reply = ''
    query = select(User).where(User.telegram_id == user_id) #смотрим в базу
    result = db_session.execute(query).scalar()
    if not result:
        user = User(telegram_id=user_id)
        db_session.add(user)
        db_session.commit()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    #self.logger.info(f"User {update.effective_user.full_name} started the bot")
    await update.message.reply_text('Отправь фотографию ценников')


async def clear_data(update: Update, context:CallbackContext)->None:
    """
    this method clear photo data
    """
    # self = context.bot_data

    user_id = context._user_id
    reply = ''
    mb_photo_data = user_data.get(user_id)
    if mb_photo_data == None:
        user_data[user_id] = list()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    reply = f"количество записей в списке: {len(user_data[user_id])} \n"
    reply += "список очищен"

    user_data[user_id].clear()
    #self.logger.info(f"User {update.effective_user.full_name} started the bot")
    await update.message.reply_text(reply)

async def calculate(update: Update, context:CallbackContext)->None:
    """
    this method calculate optimal price
    """
    # bot_data = context.bot_data

    user_id = context._user_id
    reply = ''
    mb_photo_data = user_data.get(user_id)
    if mb_photo_data == None:
        user_data[user_id] = list()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    reply = f"список содержал {len(user_data[user_id])} записи\n"
    # pass user_data[user_id] to katusha.photo_handler
    photos = user_data[user_id]
    reply += "рассчеты проведены\n"
    reply += "список url фотографий: \n "
    for photo_url in photos:
        reply += f"{photo_url}\n"
    user_data[user_id].clear()
    #self.logger.info(f"User {update.effective_user.full_name} started the bot")
    await update.message.reply_text(reply)


async def handle_photo(update: Update, context:CallbackContext):
    """
    This method accepts photo.
    """
    # self = context.bot_data
    user_id = context._user_id
    reply = ''
    mb_photo_data = user_data.get(user_id)
    if mb_photo_data == None:
        user_data[user_id] = list()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    #lisa = context.bot_data
    photo = update.message.photo[-1]

    file = await photo.get_file()
    photo_url = file.file_path
    #file = file.download_file(file_path)
    user_data[user_id].append(photo_url)
    pd_len = len(user_data[user_id])
    
    reply += f'Добавлена фотография для сравнения.\n Всего для сравнения {pd_len} фотографий'        
    #self.logger.info(f"Фото получено от: {update.effective_user.full_name}")
    await update.message.reply_text(reply)
    

async def handle_text(update: Update, context:CallbackContext):
    """
    This method asks the user to send a photo of the product price tag, if the user sent text instead of a photo.
    """
    #self.logger.info(f"Текст получен от: {update.effective_user.full_name}: {update.message.text}")
    await update.message.reply_text('Пожалуйста, отправьте именно фотографию ценника.')
