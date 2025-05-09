import asyncio
import logging
import io
import requests
from PIL import Image
from gemini_ocr import Katusha, Product
from product_class import ProductClassifier

from sqlalchemy import select

# you should generate bot_key.py with BOT_KEY = "your telegram bot key"
# and put it into gitignore
from models import User, ProcessingResult
from db import db_session
from wolf_bot_key import wolf_api_key

from telegram import Update
from telegram.constants import ParseMode

from telegram.ext import CallbackContext, ContextTypes

user_data = {}

def add_user(user_id):
    user = User(telegram_id=user_id)
    db_session.add(user)
    db_session.commit()
    message = f'Создан новый пользователь с ID {user_id} \U0001F44B \n'
    return message

def get_or_create_user(user_id):
    query = select(User).where(User.telegram_id == user_id) #смотрим в базу
    result = db_session.execute(query).scalar()
    if not result:
        message = add_user(user_id)
    message = f'пользователь с ID {user_id} \U0001F44B \n'
    return message

async def start(update: Update, context:CallbackContext)->None:
    """
    This method asks the user to send the price tag of the product.
    """

    user_id = context._user_id
    message = get_or_create_user(user_id)
    logging.info(message)
    user_data[user_id] = {"product": [], "last_type": None}
    #self.logger.info(f"User {update.effective_user.full_name} started the bot")
    await update.message.reply_text('Отправь фотографию ценников')


async def clear_data(update: Update, context:CallbackContext)->None:
    """
    this method clear photo data
    """
    user_id = context._user_id
    reply = ''
    if user_id in user_data:
        count = len(user_data[user_id])
        user_data[user_id]["product"].clear()
        user_data[user_id]["last_type"] = None    
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
        user_data[user_id] = {"product": [], "last_type": None}
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
    photo = update.message.photo[-1]

    file = await photo.get_file()

    photo_url = file.file_path   #URL фотографии на сервере Telegram
    # data = requests.get(photo_url).content  #скачиване фото
    # img = Image.open(io.BytesIO(data))  #создание объекта изображения

    pt = context.bot_data["pt"]
    photo = pt.image_from_url(photo_url)
    img_res = pt.get_data_from_image(photo)  #обработка изображения
    if None != img_res:
        if img_res.product_type != user_data[user_id]["last_type"] and user_data[user_id]["last_type"] != None:
            reply += f' Категории продуктов не совпадают.\nВы сравниваете {ProductClassifier.type_to_str(img_res.product_type)} и {ProductClassifier.type_to_str(user_data[user_id]["last_type"])} \n' 
        user_data[user_id]["product"].append(img_res)
        print(user_data)
        pd_len = len(user_data[user_id]["product"])
        reply += f'Добавлена фотография для сравнения.\nВсего для сравнения {pd_len} фотографий'     
        user_data[user_id]["last_type"] = img_res.product_type
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


async def best_product_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    products = user_data[user_id]["products"]

    if not products:
        await update.message.reply_text("У вас пока нет сохранённых товаров.")
        return

    # Найдём самый выгодный продукт
    best = min(products, key=lambda p: p.price_per_unit)

    await update.message.reply_text(
        f"Самый выгодный товар:\n\n"
        f"📦 {best.name}\n"
        f"💰 Цена за единицу: {best.price_per_unit} ₽"
    )