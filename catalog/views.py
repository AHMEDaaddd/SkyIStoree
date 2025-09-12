from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Contact


def home_view(request):
    # список продуктов для главной (с пагинацией)
    products = Product.objects.order_by("-created_at")
    paginator = Paginator(products, 8)  # по 8 карточек на страницу
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "catalog/home.html", {"page_obj": page_obj})


def product_detail_view(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


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


# ⭐ Доп. задание: форма создания товара
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]


def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("catalog:product_detail", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "catalog/product_form.html", {"form": form})