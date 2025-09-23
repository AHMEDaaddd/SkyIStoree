from django.db import models


class Post(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    body = models.TextField("Содержимое")
    preview = models.ImageField("Превью", upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    views = models.PositiveIntegerField("Просмотры", default=0)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title