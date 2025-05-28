from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('auth', views.UserViewSet, basename='auth')
router.register('ForgotPassword', views.ForgotViewSet, basename='ForgotPassword')

urlpatterns = router.urls
