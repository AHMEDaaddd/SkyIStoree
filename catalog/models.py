from django.db import models


class Category(models.Model):
    name = models.CharField("Наименование", max_length=150)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField("Наименование", max_length=150)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="products"
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self) -> str:
        return self.name