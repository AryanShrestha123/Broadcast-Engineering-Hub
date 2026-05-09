from django.db import migrations, models


def copy_content_to_body(apps, schema_editor):
    Message = apps.get_model('messaging', 'Message')
    for msg in Message.objects.all():
        msg.body = msg.content
        if not msg.subject:
            msg.subject = 'No Subject'
        msg.save(update_fields=['body', 'subject'])


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(default='No Subject', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.RunPython(copy_content_to_body, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='message',
            name='content',
        ),
    ]
