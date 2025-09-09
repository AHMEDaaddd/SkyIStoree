from catalog.models import Product
from django.shortcuts import render
from .models import Contact

def home_view(request):
    last_five = Product.objects.order_by("-created_at")[:5]
    print("Последние 5 продуктов:", [p.name for p in last_five])  # или через logger
    return render(request, "catalog/home.html", {"last_five": last_five})

def contacts_view(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()
        if name and phone and message:
            context["success"] = "Сообщение успешно отправлено!"
    context["contact"] = Contact.objects.first()
    return render(request, "catalog/contacts.html", context)