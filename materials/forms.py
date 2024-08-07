from django.forms import BooleanField, ModelForm

from materials.models import Materials


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Присваиваем новые классы в зависимости от типа поля
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MaterialsForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Materials
        exclude = ("views_count", "slug",)


