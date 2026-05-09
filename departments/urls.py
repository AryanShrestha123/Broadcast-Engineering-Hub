from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.department_view, name='department_view'),
    path('<int:department_id>/', views.department_detail_view, name='department_detail_view'),
]