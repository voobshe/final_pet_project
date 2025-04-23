import google.generativeai as genai
from google.genai import types
import PIL.Image
import io
from dataclasses import dataclass
import requests
from wolf_bot_key import wolf_api_key
import json

ip = requests.get('https://api.ipify.org').text
print(f"Ваш внешний IP: {ip}")

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

    def decode(self, image:str)->Product:
        # Открываем изображение
        image = PIL.Image.open(image)

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

        # Отправляем сжатое изображение в Gemini
        # # response = self.client.models.generate_content(
        #     model="gemini-2.0-flash",
        #     contents=["Напиши название продукта и цену за килограмм", compressed_image]
        # )
        response = self.client.generate_content(
        contents=["Распознай с фотографии название продукта и цену за килограмм. Ответь строго в JSON формате:\n\n{\"name\": \"название\", \"price_per_unit\": число}", compressed_image]
    )
        
        # todo преобразовать ответ в название продукта и его цену
        
        print(response.text)
    # Парсим JSON-ответ
        result = json.loads(response.text[8:-4])
        product = Product(result["name"], result["price_per_unit"])
        print(product)

        # res = Product("Масло", 100)
        # return res

def main():
    wolf = Katusha(wolf_api_key)
    wolf.decode("testfile.jpg")
    return 0

if __name__ == "__main__":
    ret = main()
    exit(ret)