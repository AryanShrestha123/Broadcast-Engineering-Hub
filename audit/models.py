from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from account.models import CustomUser


class AuditLogEntry(models.Model):
    HTTP_METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('OTHER', 'OTHER'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES, default='OTHER')
    path = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=45, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Log Entry'
        verbose_name_plural = 'Audit Log Entries'

    def __str__(self):
        username = self.user.username if self.user else 'System'
        return f"{self.created_at:%Y-%m-%d %H:%M:%S} | {username} | {self.method} | {self.action}"

    @classmethod
    def log(cls, user=None, action='', description='', path='', method='OTHER', ip_address='', content_object=None):
        content_type = None
        object_id = None
        if content_object is not None:
            content_type = ContentType.objects.get_for_model(content_object)
            object_id = getattr(content_object, 'pk', None)

        return cls.objects.create(
            user=user,
            action=action[:255],
            description=description[:2000],
            method=method[:10],
            path=path[:500],
            ip_address=ip_address[:45],
            content_type=content_type,
            object_id=object_id,
        )
