from rest_framework import routers, urlpatterns

from .views import UserViewSet


router = routers.DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = router.urls