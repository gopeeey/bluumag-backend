# Generated by Django 2.1.1 on 2020-08-27 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_subcategoryclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_xlarge', models.ImageField(upload_to='store_images')),
                ('image_large', models.ImageField(blank=True, upload_to='store_images')),
                ('image_nslarge', models.ImageField(blank=True, upload_to='store_images')),
                ('image_normal', models.ImageField(blank=True, upload_to='store_images')),
                ('image_medium', models.ImageField(blank=True, upload_to='store_images')),
                ('image_small', models.ImageField(blank=True, upload_to='store_images')),
                ('image_xsmall', models.ImageField(blank=True, upload_to='store_images')),
                ('caption', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_large',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_medium',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_normal',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_nslarge',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_small',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_xlarge',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='banner_xsmall',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='banner_image',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='store.Image'),
        ),
    ]
