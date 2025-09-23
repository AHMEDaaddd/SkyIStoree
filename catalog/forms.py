from __future__ import annotations

from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_WORDS
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания/редактирования продуктов с валидацией запрещённых слов
    и отрицательной цены. Также стилизует виджеты полей.
    """

    class Meta:
        model = Product
        # Не перечисляем поля жёстко, чтобы не сломать проект, если модель отличается.
        # Исключаем только служебные/авто-поля.
        exclude: list[str] = []
        # Базовые виджеты — стили докинем в __init__
        widgets = {
            # Пример: при желании можно подменить Textarea и т.д.
            # "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Стилизуем все поля (Bootstrap-like классы)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

        # Если у модели есть булево поле публикации — убедимся, что это чекбокс
        if "is_published" in self.fields and not isinstance(
            self.fields["is_published"].widget, forms.CheckboxInput
        ):
            self.fields["is_published"].widget = forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            )

    # ----- ВАЛИДАЦИЯ -----

    def _check_forbidden(self, value: str, field_label: str) -> str:
        """
        Проверяет наличие запрещённых слов (в любом регистре).
        """
        lowered = (value or "").lower()
        for bad in FORBIDDEN_WORDS:
            if bad in lowered:
                raise ValidationError(
                    f"Поле «{field_label}» содержит запрещённое слово: «{bad}».",
                    code="forbidden_word",
                )
        return value

    def clean_name(self) -> str:
        value = self.cleaned_data.get("name", "")
        return self._check_forbidden(value, self.fields["name"].label or "Название")

    def clean_description(self) -> str:
        # Описание может отсутствовать в модели — учитываем это
        if "description" not in self.fields:
            return self.cleaned_data.get("description", "")
        value = self.cleaned_data.get("description", "")
        return self._check_forbidden(
            value, self.fields["description"].label or "Описание"
        )

    def clean_price(self) -> Any:
        if "price" not in self.fields:
            return self.cleaned_data.get("price")
        price = self.cleaned_data.get("price")
        if price is None:
            return price
        # Цена не может быть отрицательной
        try:
            if price < 0:  # type: ignore[operator]
                raise ValidationError(
                    "Цена не может быть отрицательной.", code="negative_price"
                )
        except TypeError:
            # Если тип не сравним/нечисловой
            raise ValidationError("Некорректное значение цены.", code="invalid_price")
        return price

    def clean(self) -> dict[str, Any]:
        cleaned = super().clean()

        # Доп. задание: проверка изображений (если поле существует в форме)
        image_field_name = None
        for candidate in ("image", "photo", "picture"):
            if candidate in self.fields:
                image_field_name = candidate
                break

        if image_field_name:
            img = cleaned.get(image_field_name)
            if img:
                # Проверяем тип
                valid_ct = {"image/jpeg", "image/png"}
                content_type = getattr(img, "content_type", None)
                if content_type and content_type not in valid_ct:
                    self.add_error(
                        image_field_name,
                        ValidationError(
                            "Поддерживаются только изображения JPEG или PNG.",
                            code="bad_image_type",
                        ),
                    )
                # Проверяем размер (≤ 5 МБ)
                max_bytes = 5 * 1024 * 1024
                size = getattr(img, "size", None)
                if size and size > max_bytes:
                    self.add_error(
                        image_field_name,
                        ValidationError(
                            "Размер изображения не должен превышать 5 МБ.",
                            code="image_too_big",
                        ),
                    )

        return cleaned