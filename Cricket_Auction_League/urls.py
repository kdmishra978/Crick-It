"""Cricket_Auction_League URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.site.site_header = "DForce CRICKET SIMULATOR"
admin.site.site_title = "DForce Admin Portal"
admin.site.index_title = "Welcome to DForce Cricket Simulator"

urlpatterns = [
    url('', include('Home.urls')),
    url('players/', include('Players.urls')),
    url('team/', include('Teams.urls')),
    url('toss/', include('Toss.urls')),
    url('match/', include('Match.urls')),
    url('tournament/', include('Tournament.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)