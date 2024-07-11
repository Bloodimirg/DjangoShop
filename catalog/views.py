from django.shortcuts import render
from catalog.models import Product


def home(request):
    """Контроллер для главной страницы """
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'products/products_list.html', context=context)


def product_detail(request, pk):
    """Страница с товаром по ключу"""
    product = Product.objects.get(pk=pk)
    context = {"product": product}
    return render(request, template_name='products/product_detail.html', context=context)


def contacts(request):
    """Контроллер обработки страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Имя: {name} | телефон: {phone} | сообщение: {message}")
    return render(request, template_name='main/contacts.html')
