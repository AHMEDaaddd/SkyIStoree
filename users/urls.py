from django.urls import path
from .views import RegisterView, EmailLoginView, LogoutUserView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]