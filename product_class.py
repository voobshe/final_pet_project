
class ProductClassifier:
    # Статический словарь (привязан к классу)
    # Ключи - категории, значения - списки ключевых слов
    product_types = {
        "неклассифицированный": 0,
        "молоко": 1,
        "хлеб": 2,
        "яблоки": 3,
        "картофель": 4,
        "печенье": 5,
        "сосиски": 6,
        "колбаса": 6,
        "сыр": 7,
        "мандарины": 8,
        "груша": 9
    }

    type_names = {
        0:"неклассифицированный",
        1:"молочные",
        2:"хлебобулочные",
        3:"фрукты",
        4:"овощи",
        5:"бакалея",
        6:"колбасные",
        7:"сыры",
        8:"цитрусы",
        9:"груши",
    }


    @staticmethod
    def check(product_name: str) -> int:
        """
        Проверяет продукт и возвращает его класс (число)
        
        :param product_name: Название продукта для классификации
        :return: Номер категории или 0, если категория не найдена
        """
        lower_name = product_name.lower()  # Приводим к нижнему регистру
        keys = ProductClassifier.product_types.keys()
        for key in keys:
            if key in lower_name:
                return ProductClassifier.product_types[key]


    def type_to_str(pr_type:int) -> str:
        """
        Gреобразует тип продукта из int в строку
        """
        if 9 >= pr_type:
            return ProductClassifier.type_names[pr_type]
        else:
            return "неклассифицированный"


if __name__ == "__main__":
    products = name

    for product in products:
        category = ProductClassifier.check(product)
        print(f"Продукт: '{name}' -> Категория: {category}")