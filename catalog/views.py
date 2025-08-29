from django.shortcuts import render

def home_view(request):
    return render(request, 'catalog/home.html')  # рендер главной

def contacts_view(request):
    # Доп. задание: простая обработка формы без БД
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        # Здесь можно добавить любую логику/валидацию/отправку
        if name and phone and message:
            context['success'] = 'Сообщение успешно отправлено!'
    return render(request, 'catalog/contacts.html', context)