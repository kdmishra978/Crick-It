from django.urls import path
from Teams import views

urlpatterns = [
    path('get/<str:team_name>/', views.get_team_data),
    path('set/<str:team_name>/', views.set_team),
]