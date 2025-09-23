from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField("Слаг", max_length=140, unique=True, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="categories/", blank=True, null=True)
    is_published = models.BooleanField("Опубликована", default=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField("Наименование", max_length=150)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Категория",
        related_name="products",
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    is_published = models.BooleanField("Опубликован", default=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("catalog:product_detail", kwargs={"pk": self.pk})


    def __str__(self) -> str:
        return getattr(self, "name", f"Product #{self.pk}")


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    title = models.CharField("Заголовок", max_length=150, default="Контакты")
    address = models.CharField("Адрес", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("E-mail", blank=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


    def __str__(self) -> str:
        return self.title