from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),          # стандартная админка Django
    path("", include("catalog.urls")),        # маршруты из приложения catalog
]

# это для медиафайлов (картинки, фото продуктов и т.п.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)