"""Game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/

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
from django.urls import path
import game.views as views
from .decorators import game_developer_required

app_name = 'game'

#games use game to determine the pk
urlpatterns = [
    path('games/<int:game>/', views.details, name='detail'),
    path('games/<int:game>/purchase', views.purchase, name='purchase'),
    path('games/<int:game>/highscore', views.highscore, name='highscore'),
    path('games/<int:game>/delete', game_developer_required(views.GameDeleteView.as_view()), name='delete'),
    path('games/search/', views.search, name='search'),
    path('games/<int:game>/update', game_developer_required(views.GameUpdateView.as_view()), name='game_update'),
    path('games/<int:game>/update_playedgame', views.update_played_game, name='update'),
    path('games/process_purchase', views.process, name='process'),
    path('games/upload/', views.upload, name='upload'),
    path('games/<int:game>/rate', views.rate, name='rate'),
]
