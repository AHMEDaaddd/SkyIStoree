from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)

from .forms import ProductForm
from .models import Product, Category
from .services import get_products_by_category


# ------- Главная: список товаров (низкоуровневый кеш) -------
class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        cache_key = "home:products"
        if settings.CACHE_ENABLED:
            data = cache.get(cache_key)
            if data is not None:
                return data

        qs = (
            Product.objects.filter(is_published=True)
            .select_related("category", "owner")
            .order_by("-updated_at")
        )
        products = list(qs)

        if settings.CACHE_ENABLED:
            cache.set(cache_key, products, timeout=None)  # можно задать TIMEOUT из настроек

        return products


# ------- Товары -------
# Кеш страницы товара на 5 минут (если включён CACHE_ENABLED)
def _cache_decorator():
    if settings.CACHE_ENABLED:
        return method_decorator(cache_page(60 * 5), name="dispatch")
    # пустой декоратор, если кеш выключен
    def passthrough(cls):
        return cls
    return passthrough


@_cache_decorator()
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
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        return u.is_superuser or obj.owner_id == u.id


class OwnerOrModeratorDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        if obj.owner_id == u.id:
            return True
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
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save(update_fields=["is_published", "updated_at"])
            # Чистим кеши, связанные с листингами и деталкой
            if settings.CACHE_ENABLED:
                cache.delete("home:products")
                cache.delete_pattern(f"category:{product.category_id}:*")
                cache.delete(f"views.decorators.cache.cache_page.{request.get_full_path()}")
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


# Новое отдельное представление: продукты выбранной категории
class CategoryProductsView(TemplateView):
    template_name = "catalog/category_products.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs["pk"])
        products = get_products_by_category(category.id, only_published=True)
        ctx["category"] = category
        ctx["products"] = products
        return ctx