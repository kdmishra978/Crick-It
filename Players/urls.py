from django.urls import path
from Players import views

urlpatterns = [
    path("", views.players_page, name='players'),
    path("<str:view>/", views.display_players),
    path("<str:view>/<str:name>/", views.view_player),
    
    path("<str:view>/sort/<str:sort_type>/", views.sort_players),
]