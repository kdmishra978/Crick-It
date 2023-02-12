from django.urls import path
from Tournament import views

urlpatterns = [
    path('start/', views.starttournament_page),
    path('<str:name>/', views.base, name="base"),
    path('<str:name>/pointstable/', views.pointstable, name="points"),
    path('<str:name>/auction/', views.auction, name="points"),
]