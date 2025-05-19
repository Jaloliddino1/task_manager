from django.urls import path
from task_manager import views

urlpatterns = [
    path('', views.HelloAPIView.as_view(), name='hello'),
    path('project/', views.ProjectAPIView.as_view(), name='hello'),
    path('project/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='hello')
]
