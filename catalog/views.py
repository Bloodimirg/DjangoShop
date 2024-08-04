from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from catalog.models import Product, Version
from catalog.forms import ProductForm, VersionForm


class ProductCreateView(CreateView):
    """Создание продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    """Список продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['object_list']
        for product in products:
            active_version = product.versions.filter(is_current=True).first()
            if active_version:
                product.active_version = active_version
        return context


class ProductDetailView(DetailView):
    """Просмотр одного продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'


class ProductUpdateView(UpdateView):
    """Редактирование продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    # создания и добавления формы с инлайн-набором форм (formset) для модели Version, связанной с моделью Product
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    # Если валидация проходит успешно, данные сохраняются.
    # В противном случае, метод возвращает ответ с невалидными формами, чтобы пользователь мог исправить ошибки.
    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    """Удаление продукта"""
    model = Product
    success_url = reverse_lazy('catalog:home')
    template_name = 'catalog/product_confirm_delete.html'


class ContactsView(View):
    """Просмотр страницы контактов"""

    def get(self, request):
        return render(request, template_name='catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Имя: {name} | телефон: {phone} | сообщение: {message}")
        # Здесь можно добавить логику обработки данных формы
        return render(request, template_name='catalog/contacts.html')
