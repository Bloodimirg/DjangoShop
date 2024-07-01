from django.db import models

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["description", "name"]

    def __str__(self):
        return {self.name}


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
    )
    image = models.ImageField(upload_to="catalog/photo", **NULLABLE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите название категории",
        **NULLABLE,
        related_name="products"
    )
    purchase_price = models.IntegerField(**NULLABLE, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["description", "name"]

    def __str__(self):
        return {self.name}
