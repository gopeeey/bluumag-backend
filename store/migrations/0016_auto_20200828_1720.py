# Generated by Django 2.1.1 on 2020-08-28 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20200827_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, to='store.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='subcategories',
            field=models.ManyToManyField(blank=True, to='store.SubCategory'),
        ),
    ]