# Generated by Django 2.1.1 on 2020-09-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_image_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
