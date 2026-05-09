from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='messages_inbox'),
    path('sent/', views.sent_messages, name='messages_sent'),
    path('drafts/', views.drafts, name='messages_drafts'),
    path('compose/', views.compose_message, name='messages_compose'),
    path('<int:message_id>/', views.view_message, name='message_detail'),
    path('<int:message_id>/delete/', views.delete_message, name='message_delete'),
]