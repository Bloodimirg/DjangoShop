from django.core.exceptions import ValidationError
from django.forms import ModelForm

from catalog.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

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