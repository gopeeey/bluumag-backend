# Generated by Django 2.1.1 on 2020-09-10 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_auto_20200910_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='homepage_banner',
            field=models.BooleanField(default=False),
        ),
    ]