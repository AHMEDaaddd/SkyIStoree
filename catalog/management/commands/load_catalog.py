from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = "Очищает таблицы и загружает фикстуры категорий и продуктов"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        call_command("loaddata", "categories.json", "products.json")
        self.stdout.write(self.style.SUCCESS("Фикстуры успешно загружены"))