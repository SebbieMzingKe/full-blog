# Generated by Django 4.2.16 on 2024-10-27 14:45

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0002_alter_post_author'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('models', django.db.models.manager.Manager()),
            ],
        ),
    ]
