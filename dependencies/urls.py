from django.urls import path
from . import views

app_name = 'dependencies'

urlpatterns = [
    path('', views.dependency_list, name='dependency_list'),
    path('create/', views.dependency_create, name='dependency_create'),
    path('<int:pk>/update/', views.dependency_update, name='dependency_update'),
    path('<int:pk>/delete/', views.dependency_delete, name='dependency_delete'),
]