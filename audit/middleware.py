import json
from .models import AuditLogEntry


class AuditLogMiddleware:
    EXEMPT_PATH_PREFIXES = [
        '/static/',
        '/admin/',
        '/notifications/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.log_request(request, response)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')

    def should_log(self, request):
        if not request.user.is_authenticated:
            return False

        path = request.path
        for prefix in self.EXEMPT_PATH_PREFIXES:
            if path.startswith(prefix):
                return False
        if request.method not in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'):
            return False
        return True

    def log_request(self, request, response):
        if not self.should_log(request):
            return

        description = ''
        try:
            if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
                if request.content_type == 'application/json':
                    payload = json.loads(request.body.decode('utf-8') or '{}')
                    description = json.dumps(payload, ensure_ascii=False)
                else:
                    description = dict(request.POST)
            elif request.method == 'GET':
                description = dict(request.GET)
        except Exception:
            description = ''

        AuditLogEntry.log(
            user=request.user,
            action=f"{request.method} {request.path}",
            description=str(description),
            path=request.path,
            method=request.method,
            ip_address=self.get_client_ip(request),
        )
