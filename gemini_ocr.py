import google.generativeai as genai
from google.genai import types
import PIL.Image
import io
from dataclasses import dataclass
import requests
from wolf_bot_key import wolf_api_key
import json

DEBUG_FILE = "testfile.jpg"
DEBUG_URL = "https://i.ibb.co/7tFvfD7K/testfile.jpg"

#url = 'http://example.com/img.jpg'
#data = requests.get(url).content
#img = Image.open(io.BytesIO(data))


@dataclass
class Product:
    """
    класс хранения информации о товаре
    
    Attributes: 
    name(str): название товара
    price_per_unit(float): цена за единицу товара
    """
    name:str
    price_per_unit:float

class Katusha:
    """
    Класс распознавания ценников
    Методы:
    decode
        преобразовать фотографию ценника в класс товара
        
    """
    def __init__(self, key:str):
        genai.configure(api_key=key)
        self.client = genai.GenerativeModel("gemini-2.0-flash")

    def decode(self, compressed_image)->Product:
        response = self.client.generate_content(
            contents=["Распознай с фотографии название продукта и цену за килограмм. Ответь строго в JSON формате:\n\n{\"name\": \"название\", \"price_per_unit\": число}", compressed_image]
        )
        
        # print(response.text)
        # Парсим JSON-ответ
        result = json.loads(response.text)
        product = Product(result["name"], result["price_per_unit"])
        return product


    def image_from_disk(self, image_path:str):
         # Открываем изображение
        image = PIL.Image.open(image_path)

        # Задаём максимальную ширину
        max_width = 800
        if image.width > max_width:
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            image = image.resize(new_size, PIL.Image.LANCZOS)

        # Сохраняем в память как сжатый JPEG
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG', quality=75)  # можно выставить quality 60-80
        image_bytes.seek(0)

        # Загружаем сжатое изображение обратно в PIL для передачи
        compressed_image = PIL.Image.open(image_bytes)
        return compressed_image

    def image_from_url(self, data):
        data = requests.get(DEBUG_URL).content
        image = PIL.Image.open(io.BytesIO(data))

        # Задаём максимальную ширину
        max_width = 800
        if image.width > max_width:
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            image = image.resize(new_size, PIL.Image.LANCZOS)

        # Сохраняем в память как сжатый JPEG
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG', quality=75)  # можно выставить quality 60-80
        image_bytes.seek(0)

        # Загружаем сжатое изображение обратно в PIL для передачи
        compressed_image = PIL.Image.open(image_bytes)
        return compressed_image

def main():
    """
    todo: add comment
    """
    global DEBUG_FILE
    global DEBUG_URL

    ip = requests.get('https://api.ipify.org').text
    print(f"Ваш внешний IP: {ip}")
    wolf = Katusha(wolf_api_key)

    # From file
    compressed_image = wolf.image_from_disk(DEBUG_FILE)
    file_product = wolf.decode(compressed_image)
    print(f"Продукт из файла {file_product}")

    # From url
    compressed_image = wolf.image_from_url(DEBUG_URL)
    url_product = wolf.decode(compressed_image)
    print(f"Продукт по ссылке {url_product}")
    return 0


if __name__ == "__main__":
    ret = main()
    exit(ret)