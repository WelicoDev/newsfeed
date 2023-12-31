# Generated by Django 4.2.2 on 2023-07-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_rename_contactmodel_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug_news',
            field=models.SlugField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=250),
        ),
    ]
