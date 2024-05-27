# Generated by Django 5.0.3 on 2024-05-03 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_message_group_message_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='project',
        ),
        migrations.RemoveField(
            model_name='project',
            name='description',
        ),
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.group'),
        ),
    ]
