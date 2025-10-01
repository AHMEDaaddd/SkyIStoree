from django.urls import path
from .views import (
    HomeView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductUnpublishView,
    CategoryListView,
    CategoryProductsView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # Категории
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<int:pk>/", CategoryProductsView.as_view(), name="category_detail"),

    # Товары
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),

    # Модерация публикации
    path("products/<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish"),
]