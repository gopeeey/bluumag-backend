# Generated by Django 2.1.1 on 2020-08-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, unique=True),
        ),
    ]
