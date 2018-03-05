"""Api URL Configuration"""

from django.urls import path
import api.views as views

from rest_framework import routers

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'(?P<version>v1)/users', views.UserViewSet, base_name='user')
router.register(r'(?P<version>v1)/developers', views.DeveloperViewSet, base_name='developer')
router.register(r'(?P<version>v1)/games', views.GameViewSet, base_name='game')

urlpatterns = router.urls
