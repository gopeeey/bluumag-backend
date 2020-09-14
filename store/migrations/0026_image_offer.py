# Generated by Django 2.1.1 on 2020-09-13 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_auto_20200913_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='offer',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='store.Offer'),
        ),
    ]