# Generated by Django 2.1.1 on 2020-09-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_remove_specification_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, unique=True),
        ),
    ]