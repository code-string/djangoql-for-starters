from rest_framework import routers, urlpatterns
from django.urls import path

from .views import UserViewSet, LoginView


router = routers.DefaultRouter()
router.register('user/signup', UserViewSet)
urlpatterns = [
    path('user/login/', LoginView.as_view())
]


urlpatterns += router.urls