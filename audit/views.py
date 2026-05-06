from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import AuditLogEntry


def user_is_audit_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'Admin')


def audit_admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not user_is_audit_admin(request.user):
            raise PermissionDenied('You do not have access to the audit log.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@audit_admin_required
def audit_log_list(request):
    query = request.GET.get('q', '').strip()
    method = request.GET.get('method', '').strip().upper()
    logs = AuditLogEntry.objects.all()

    if query:
        logs = logs.filter(
            Q(action__icontains=query) |
            Q(description__icontains=query) |
            Q(path__icontains=query) |
            Q(user__username__icontains=query)
        )

    if method:
        logs = logs.filter(method=method)

    logs = logs.order_by('-created_at')[:250]

    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    return render(request, 'audit/audit_log_list.html', {
        'logs': logs,
        'methods_list': METHODS,
        'query': query,
        'method': method,
        'active_page': 'audit',
    })


@audit_admin_required
def audit_log_delete(request, pk):
    log_entry = get_object_or_404(AuditLogEntry, pk=pk)
    if request.method == 'POST':
        log_entry.delete()
        messages.success(request, 'Audit log entry deleted.')
        return redirect('audit:log_list')

    return render(request, 'audit/audit_log_confirm_delete.html', {
        'log_entry': log_entry,
        'active_page': 'audit',
    })
