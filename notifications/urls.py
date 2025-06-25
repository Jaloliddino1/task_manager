from rest_framework.routers import DefaultRouter

from notifications import views

router = DefaultRouter()
router.register('notification', views.NotificationViewSet, basename='notification')

urlpatterns = router.urls
