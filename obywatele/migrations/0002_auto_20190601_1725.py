# Generated by Django 2.0.12 on 2019-06-01 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obywatele', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]