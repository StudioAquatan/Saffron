# Generated by Django 2.1.4 on 2019-01-05 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='user',
            name='joined',
        ),
    ]
