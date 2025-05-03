import asyncio
import logging
import io
import requests
from PIL import Image


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
    user_id = context._user_id
    reply = ''
    query = select(User).where(User.telegram_id == user_id) #смотрим в базу
    result = db_session.execute(query).scalar()

    if not result:
        user = User(telegram_id=user_id)
        db_session.add(user)
        db_session.commit()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    if user_id in user_data:
        count = len(self.user_data[user_id])
        self.user_data[user_id].clear()
        reply += f"Количество очищенных записей: {count}\nСписок фотографий очищен"
    else:
        reply += "Нет фотографий для очистки \U0001F625"        
    await update.message.reply_text(reply)

    
async def calculate(update: Update, context:CallbackContext)->None:
    """
    this method calculate optimal price
    """

    user_id = context._user_id
    reply = ''
    query = select(User).where(User.telegram_id == user_id) #смотрим в базу
    result = db_session.execute(query).scalar()
    if not result:
        user_data[user_id] = list()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    if len(user_data[user_id]) > 0:
        best_product = user_data[user_id][0]
        for sel in user_data[user_id]:
            if sel.price_per_unit < best_product.price_per_unit:
                best_product = sel
        reply += f"Лучший товар: {best_product}.\n"
    else:
        reply += 'Товара не выбрано.'

    user_data[user_id].clear()

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context:CallbackContext):
    """
    This method accepts photo.
    """
    # self = context.bot_data
    user_id = context._user_id
    reply = ''
    query = select(User).where(User.telegram_id == user_id) #смотрим в базу
    result = db_session.execute(query).scalar()
    if not result:
        user_data[user_id] = list()
        reply = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'

    photo = update.message.photo[-1]

    file = await photo.get_file()

    photo_url = file.file_path   #URL фотографии на сервере Telegram
    data = requests.get(photo_url).content  #скачиване фото
    img = Image.open(io.BytesIO(data))  #создание объекта изображения
    maybe_good = katusha(img)  #обработка изображения
    if None != maybe_good:
        user_data[user_id].append(maybe_good)
        pd_len = len(user_data[user_id])
        reply += f'Добавлена фотография для сравнения.\n Всего для сравнения {pd_len} фотографий'     
    else:
        reply += 'Ценник не распознан.'   
    #self.logger.info(f"Фото получено от: {update.effective_user.full_name}")
    await update.message.reply_text(reply)
    

async def handle_text(update: Update, context:CallbackContext):
    """
    This method asks the user to send a photo of the product price tag, if the user sent text instead of a photo.
    """
    #self.logger.info(f"Текст получен от: {update.effective_user.full_name}: {update.message.text}")
    await update.message.reply_text('Пожалуйста, отправьте именно фотографию ценника.')
