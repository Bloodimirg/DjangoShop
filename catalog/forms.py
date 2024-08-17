from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, forms

from catalog.models import Product, Version


class StyleFormMixin:
    """Миксин для стилизации форм"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Присваиваем новые классы в зависимости от типа поля
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    """Модель для фильтрации слов при создании товара"""

    class Meta:
        model = Product
        exclude = 'user',

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        name = self.cleaned_data.get('name')
        for word in forbidden_words:
            if word in name.lower():
                raise ValidationError('Название продукта содержит запрещенное слово.')
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        description = self.cleaned_data.get('description')
        for word in forbidden_words:
            if word in description.lower():
                raise ValidationError('Описание продукта содержит запрещенное слово.')
        return description


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')


class VersionForm(StyleFormMixin, ModelForm):
    """Форма версии продукта"""
    class Meta:
        model = Version
        fields = "__all__"
