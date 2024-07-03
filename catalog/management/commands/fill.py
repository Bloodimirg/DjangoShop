import json
from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """Читаем фикстуру категории"""
        with open('catalog/fixtures/category.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        """Читаем фикстуру продукты"""
        with open('catalog/fixtures/product.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        # очищаем категории и товары
        Product.truncate_table_restart_id()
        Category.truncate_table_restart_id()

        product_for_create = []
        category_for_create = []

        # цикл по фикстуре категорий
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(**category['fields'])
            )

        # создаем категорию товара
        Category.objects.bulk_create(category_for_create)

        # цикл по фикстуре товаров
        for product in Command.json_read_products():
            product_for_create.append(
                Product(name=product['fields']['name'],
                        description=product['fields']['description'],
                        image=product['fields']['image'],
                        purchase_price=product['fields']['purchase_price'],
                        category=Category.objects.get(pk=product['fields']['category'])
                        ))
        # создаем товары
        Product.objects.bulk_create(product_for_create)
