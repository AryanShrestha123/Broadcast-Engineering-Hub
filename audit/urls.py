from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_log_list, name='log_list'),
    path('<int:pk>/delete/', views.audit_log_delete, name='delete_log'),
]
