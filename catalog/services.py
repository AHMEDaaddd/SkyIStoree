from django.conf import settings
from django.core.cache import cache

from .models import Product


def get_products_by_category(category_id: int, only_published: bool = True, ttl: int | None = None):
    """
    Возвращает список продуктов указанной категории.
    Результат кешируется низкоуровнево (cache.get/set).

    :param category_id: ID категории
    :param only_published: Только опубликованные продукты
    :param ttl: Время жизни кеша в секундах (если None, берём стандартный TIMEOUT)
    """
    qs_key = f"category:{category_id}:published:{int(only_published)}"

    if settings.CACHE_ENABLED:
        data = cache.get(qs_key)
        if data is not None:
            return data

    qs = Product.objects.select_related("category", "owner").filter(category_id=category_id)
    if only_published:
        qs = qs.filter(is_published=True)
    qs = qs.order_by("-updated_at")

    products = list(qs)

    if settings.CACHE_ENABLED:
        cache.set(qs_key, products, timeout=ttl)

    return products