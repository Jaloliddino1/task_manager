from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register('auth', views.UserViewSet, basename='auth')

urlpatterns = [
                  path('login_jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ]+router.urls
