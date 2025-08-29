# Skystore (Django)

Учебный проект интернет-магазина (шаблоны: главная и контакты).

## Стек
- Python 3.10+
- Django 5.x
- Bootstrap 5 (CDN)

## Установка
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
Запуск
bash
Копировать код
python manage.py runserver
Открой:

Главная: http://127.0.0.1:8000/

Контакты: http://127.0.0.1:8000/contacts/

Структура
core/ — проект, INSTALLED_APPS, urls

catalog/ — приложение (views, urls, templates)

GitFlow
Работа ведётся в ветках feature/* → PR в develop. Релизы — из develop в main.

yaml
Копировать код

---

# 9) GitFlow: ветки, коммиты, PR

```bash
# инициализация репозитория
git init
git add .
git commit -m "Init Django project: core, catalog, templates, urls, views"

# создать удалённый репозиторий (на GitHub создай репо и подставь URL)
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main

# создать develop от main
git checkout -b develop
git push -u origin develop

# ветка домашки (пример)
git checkout -b feature/hw-01-setup
# ... правки ...
git add .
git commit -m "HW-01: add catalog app, urls, templates, contact form handling"
git push -u origin feature/hw-01-setup

# На GitHub: создаёшь Pull Request из feature/hw-01-setup → develop
Домашка сдаётся через Pull Request из ветки домашней работы в develop — это выполняет критерий.