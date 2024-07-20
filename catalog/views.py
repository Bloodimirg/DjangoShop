from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, CreateView

from catalog.models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactsView(View):
    def get(self, request):
        return render(request, template_name='catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Имя: {name} | телефон: {phone} | сообщение: {message}")
        # Здесь можно добавить логику обработки данных формы
        return render(request, template_name='catalog/contacts.html')

# class ProductCreateView(CreateView):
#     model = Product
#     fields = ("name", "description", "image", )
