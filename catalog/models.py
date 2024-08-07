from django.db import models, connection

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE"
            )

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
        return f"{self.name}"


class Product(models.Model):
    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE"
            )

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
        related_name="products",
    )
    purchase_price = models.IntegerField(**NULLABLE, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["description", "name"]

    def __str__(self):
        return f"{self.name}"


class Version(models.Model):
    product = models.ForeignKey(
        Product, related_name="versions", on_delete=models.SET_NULL, **NULLABLE
    )
    version_number = models.CharField(max_length=50, verbose_name="Номер версии")
    version_name = models.CharField(max_length=255, verbose_name="Название версии")
    is_current = models.BooleanField(default=False, verbose_name="Текущая версия")

    class Meta:
        ordering = ["-is_current", "version_number"]
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

        # ограничение полей product и current_version,
        # гарантия того, что для каждого продукта может быть только одна текущая версия.
        constraints = [
            models.UniqueConstraint(
                fields=["product", "is_current"],
                condition=models.Q(is_current=True),
                name="unique_current_version",
            )
        ]

    def __str__(self):
        return f"{self.version_name} (v{self.version_number})"
