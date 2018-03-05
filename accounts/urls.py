"""Account URL Configuration

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
from django.contrib.auth import views as auth_views
from .views import RegisterView, ActivationView, HomeView, ChooseGroupView, ProfileUpdateView, ProfileDetailView, \
    ProfileStatisticsView

from game.decorators import profile_owner_required

app_name = 'accounts'

#accounts use pk to determine the pk whereas games require game
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('accounts/choosegroup', ChooseGroupView.as_view(), name="choosegroup" ),
    path('accounts/<int:pk>', profile_owner_required(ProfileDetailView.as_view()), name='detail' ),
    path('accounts/<int:pk>/update', profile_owner_required(ProfileUpdateView.as_view()), name='update'),
    path('accounts/activate/<token>', ActivationView.as_view(), name='activate'),
    path('accounts/register', RegisterView.as_view(template_name='accounts/register.html', success_url='home'), name='register'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('accounts/<int:pk>/<int:game>', profile_owner_required(ProfileStatisticsView.as_view()), name='statistics')
]
