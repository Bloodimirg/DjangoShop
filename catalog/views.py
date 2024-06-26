from django.shortcuts import render


def home(request):
    """Контроллер для главной страницы """
    return render(request, 'main/home.html')


def contacts(request):
    """Контроллер обработки страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Имя: {name} телефон: {phone} сообщение: {message}")
    return render(request, template_name='main/contacts.html')

