# Generated by Django 4.2.16 on 2024-10-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0003_alter_post_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date='publish'),
        ),
    ]