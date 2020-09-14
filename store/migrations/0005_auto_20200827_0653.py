# Generated by Django 2.1.1 on 2020-08-27 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200827_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item_variant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.ItemVariant'),
        ),
        migrations.AlterField(
            model_name='image',
            name='subcategory',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banner_image', to='store.SubCategory'),
        ),
    ]