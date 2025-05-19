from django.urls import path
from task_manager import views
urlpatterns=[
    path('',views.HelloAPIViev.as_view(),name='helo'),

    path('project',views.ProjectAPIView.as_view(),name='helo'),
    path('project/<int:pk>',views.ProjectDetailAPIViev.as_view(),name='helo'),
    path('project', views.HelloAPIViev.as_view(), name='helo'),
]