from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группы и назначает права (Модератор продуктов, опционально Контент-менеджер)."

    def handle(self, *args, **options):
        # --- Права для продуктов ---
        product_ct = ContentType.objects.get_for_model(Product)

        # Кастомное право на снятие с публикации (создано через Meta.permissions в модели)
        can_unpublish_perm, _ = Permission.objects.get_or_create(
            content_type=product_ct,
            codename="can_unpublish_product",
            defaults={"name": "Can unpublish product"},
        )

        # Базовое право на удаление продукта
        try:
            delete_perm = Permission.objects.get(content_type=product_ct, codename="delete_product")
        except Permission.DoesNotExist:
            self.stderr.write(self.style.ERROR("Право delete_product не найдено. Выполните миграции."))
            return

        # --- Группа Модератор продуктов ---
        moderators, _ = Group.objects.get_or_create(name="Модератор продуктов")
        moderators.permissions.add(can_unpublish_perm, delete_perm)
        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' настроена."))

        # --- Доп. задание: Контент-менеджер для блога ---
        # Настроим, если есть блог и модель Post
        try:
            from blog.models import Post  # noqa
            post_ct = ContentType.objects.get(app_label="blog", model="post")
            perms = Permission.objects.filter(
                content_type=post_ct,
                codename__in=["add_post", "change_post", "delete_post"],
            )
            content_mgr, _ = Group.objects.get_or_create(name="Контент-менеджер")
            content_mgr.permissions.add(*list(perms))
            self.stdout.write(self.style.SUCCESS("Группа 'Контент-менеджер' настроена."))
        except Exception:
            self.stdout.write("Блог не найден или модель Post отсутствует — пропускаю настройку 'Контент-менеджер'.")