# Generated by Django 4.2.2 on 2023-07-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_rename_users_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]