# Generated by Django 5.0.3 on 2024-05-02 18:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_group_participants'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='project_participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
