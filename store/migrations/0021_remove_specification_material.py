# Generated by Django 2.1.1 on 2020-08-29 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_item_item_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specification',
            name='material',
        ),
    ]