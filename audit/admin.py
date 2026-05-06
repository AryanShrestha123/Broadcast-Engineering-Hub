from django.contrib import admin
from .models import AuditLogEntry


@admin.register(AuditLogEntry)
class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'method', 'action', 'path', 'ip_address')
    list_filter = ('method', 'created_at', 'user')
    search_fields = ('action', 'description', 'path', 'user__username', 'ip_address')
    readonly_fields = ('user', 'action', 'description', 'method', 'path', 'ip_address', 'content_type', 'object_id', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
