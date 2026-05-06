from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import AuditLogEntry
from departments.models import Department
from schedule.models import MeetingSchedule
from teams.models import Team

User = get_user_model()


def _get_username(user):
    if user is None:
        return 'None'
    return getattr(user, 'username', str(user))


@receiver(post_save, sender=User)
def log_new_user_created(sender, instance, created, **kwargs):
    if not created:
        return

    AuditLogEntry.log(
        user=instance,
        action='New user created',
        description=f'User "{_get_username(instance)}" was created.',
        method='OTHER',
        path='',
        ip_address='',
        content_object=instance,
    )


@receiver(post_save, sender=Department)
def log_department_created(sender, instance, created, **kwargs):
    if not created:
        return

    AuditLogEntry.log(
        action='Department created',
        description=(
            f'Department "{instance.departmentName}" created '
            f'with leader "{_get_username(instance.departmentLeader)}".'
        ),
        method='OTHER',
        path='',
        ip_address='',
        content_object=instance,
    )


@receiver(pre_save, sender=Department)
def log_department_leader_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        previous = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if previous.departmentLeader_id != instance.departmentLeader_id:
        AuditLogEntry.log(
            action='Department leader changed',
            description=(
                f'Department "{instance.departmentName}" leader changed from '
                f'"{_get_username(previous.departmentLeader)}" to "{_get_username(instance.departmentLeader)}".'
            ),
            method='OTHER',
            path='',
            ip_address='',
            content_object=instance,
        )


@receiver(post_save, sender=Team)
def log_team_created(sender, instance, created, **kwargs):
    if not created:
        return

    AuditLogEntry.log(
        action='Team created',
        description=f'Team "{instance.teamName}" created.',
        method='OTHER',
        path='',
        ip_address='',
        content_object=instance,
    )


@receiver(pre_save, sender=Team)
def log_team_leader_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        previous = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if previous.teamLeader_id != instance.teamLeader_id:
        AuditLogEntry.log(
            action='Team leader changed',
            description=(
                f'Team "{instance.teamName}" leader changed from '
                f'"{_get_username(previous.teamLeader)}" to "{_get_username(instance.teamLeader)}".'
            ),
            method='OTHER',
            path='',
            ip_address='',
            content_object=instance,
        )


@receiver(post_save, sender=MeetingSchedule)
def log_meeting_added(sender, instance, created, **kwargs):
    if not created:
        return

    AuditLogEntry.log(
        user=instance.createdBy,
        action='Meeting added',
        description=(
            f'Meeting "{instance.meetingTitle}" scheduled for {instance.meetingDate} '
            f'by "{_get_username(instance.createdBy)}".'
        ),
        method='OTHER',
        path='',
        ip_address='',
        content_object=instance,
    )
