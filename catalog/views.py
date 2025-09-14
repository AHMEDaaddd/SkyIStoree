from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Product, Contact


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"      # в шаблоне будем итерироваться по page_obj.object_list
    paginate_by = 8

    def get_queryset(self):
        # последние товары первыми
        return Product.objects.order_by("-created_at")


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contact"] = Contact.objects.first()
        return ctx

    def post(self, request, *args, **kwargs):
        # имитируем «успешную отправку», показываем alert
        ctx = self.get_context_data(**kwargs)
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()
        if name and phone and message:
            ctx["success"] = "Сообщение успешно отправлено!"
        return self.render_to_response(ctx)