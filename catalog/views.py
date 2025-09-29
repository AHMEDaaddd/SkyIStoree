from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)

from .forms import ProductForm
from .models import Product, Category


# ------- Каталог / Главная -------
class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return (
            Product.objects.filter(is_published=True)
            .select_related("category", "owner")
            .order_by("-updated_at")
        )


# ------- Товары -------
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        # Привязываем владельца
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerOnlyMixin(UserPassesTestMixin):
    """Доступ только владельцу объекта (или суперпользователю)."""

    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        return u.is_superuser or obj.owner_id == u.id


class OwnerOrModeratorDeleteMixin(UserPassesTestMixin):
    """Удалять может владелец, модератор продуктов или суперпользователь."""

    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        if obj.owner_id == u.id:
            return True
        # Группа модераторов
        return u.groups.filter(name="Модератор продуктов").exists()


class ProductUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorDeleteMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


class ProductUnpublishView(PermissionRequiredMixin, View):
    """Снять продукт с публикации (для модераторов)."""
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save(update_fields=["is_published", "updated_at"])
            messages.success(request, "Продукт снят с публикации.")
        else:
            messages.info(request, "Продукт уже снят с публикации.")
        return redirect(product.get_absolute_url())


# ------- Категории -------
class CategoryListView(TemplateView):
    template_name = "catalog/category_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all().order_by("name")
        return ctx


class CategoryDetailView(ListView):
    model = Product
    template_name = "catalog/category_detail.html"
    context_object_name = "products"

    def get_queryset(self):
        return (
            Product.objects.filter(category_id=self.kwargs["pk"], is_published=True)
            .select_related("category", "owner")
            .order_by("-updated_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = get_object_or_404(Category, pk=self.kwargs["pk"])
        return ctx