from django.urls import path
from Home import views

urlpatterns = [
    path("", views.home_page, name='home'),
    path("refresh/", views.refresh),
]