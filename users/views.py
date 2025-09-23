from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import User

from .forms import UserRegisterForm, EmailAuthenticationForm


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = form.save()
        # Автовход после регистрации (можно отключить, если не нужно)
        login(self.request, user)

        # Отправляем приветственное письмо
        try:
            send_mail(
                subject="Добро пожаловать в Skystore!",
                message="Вы успешно зарегистрировались. Приятных покупок!",
                from_email=None,  # возьмётся из DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            # не падаем на dev-окружении
            pass

        messages.success(self.request, "Регистрация прошла успешно. Добро пожаловать!")
        return super().form_valid(form)


class EmailLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = EmailAuthenticationForm


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("catalog:home")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("username", "avatar", "phone", "country")  # email не редактируем
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("catalog:home")


    def get_object(self, queryset=None):
        return self.request.user