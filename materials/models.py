from django.db import models

NULLABLE = {"blank": True, "null": True}


class Materials(models.Model):
    """Модель для создания блога"""
    title = models.CharField(max_length=150,
                             verbose_name="Название"
                             )

    slug = models.CharField(max_length=150, null=True, blank=True, verbose_name='slug')
    body = models.TextField(max_length=150, verbose_name="Содержимое")
    image = models.ImageField(upload_to="materials/photo", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'


