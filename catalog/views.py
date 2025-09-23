from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return (
            Product.objects.filter(is_published=True)
            .select_related("category")
            .order_by("-updated_at")
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


class CategoryListView(TemplateView):
    template_name = "catalog/category_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all().order_by("name")
        return ctx


class CategoryDetailView(ListView):
    """Список товаров выбранной категории."""
    model = Product
    template_name = "catalog/category_detail.html"
    context_object_name = "products"

    def get_queryset(self):
        return (
            Product.objects.filter(category_id=self.kwargs["pk"], is_published=True)
            .select_related("category")
            .order_by("-updated_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = Category.objects.get(pk=self.kwargs["pk"])
        return ctx