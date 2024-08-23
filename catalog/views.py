from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from catalog.models import Product, Version
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm


class ProductCreateView(CreateView, LoginRequiredMixin):
    """Создание продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Привязываем текущего пользователя к продукту
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    """Список продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['object_list']
        for product in products:
            active_version = product.versions.filter(is_current=True).first()
            if active_version:
                product.active_version = active_version
        return context


class ProductDetailView(DetailView, LoginRequiredMixin):
    """Просмотр одного продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_version = product.versions.filter(is_current=True).first()
        if active_version:
            product.active_version = active_version
        context['object'] = product

        return context


class ProductUpdateView(UpdateView, LoginRequiredMixin):
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

    def get_form_class(self):
        user = self.request.user

        # Superuser - может редактировать все поля у всех
        if user.is_superuser:
            return ProductForm
        # user - может редактировать все поля только если является владельцем
        if user == self.object.user:
            return ProductForm
        # moderator - может редактировать только определенные поля у всех, И все поля если является владельцем продукта
        if user.has_perm('catalog.can_change_description') and user.has_perm(
                'catalog.can_change_category') and user.has_perm('catalog.can_change_is_published'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(DeleteView, LoginRequiredMixin):
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
