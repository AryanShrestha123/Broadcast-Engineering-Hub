from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('sign-up/', views.signup_view, name='signup_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('password-reset/', views.password_reset_view, name='password_reset_view'),
    path('notifications/', views.login_view, name='notifications_view'),
]