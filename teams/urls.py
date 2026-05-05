from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_view, name='team_view'),
    path('<int:team_id>/', views.team_detail_view, name='team_detail_view'),
    path('create/', views.team_create_view, name='team_create_view'),
    path('<int:team_id>/edit/', views.team_edit_view, name='team_edit_view'),
]