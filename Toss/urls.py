from django.urls import path
from Toss import views

urlpatterns = [
    path('<str:team1>/<str:team2>/', views.handle_toss),
]