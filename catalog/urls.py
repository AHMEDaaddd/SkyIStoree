from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),             # "/" или "home/"
    path('contacts/', views.contacts_view, name='contacts'),  # "contacts/"
]