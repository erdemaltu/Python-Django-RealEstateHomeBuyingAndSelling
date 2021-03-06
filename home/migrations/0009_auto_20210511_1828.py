# Generated by Django 3.2 on 2021-05-11 15:28

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210407_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='home',
            name='building_age',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='home',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='dues',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='floor_location',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='keywords',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='home',
            name='number_of_floors',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='number_of_rooms',
            field=models.CharField(blank=True, choices=[('Default', 'Belirtilmemiş'), ('1', '1+1'), ('2', '2+1'), ('3', '3+1'), ('4', '4+1')], default='Default', max_length=30),
        ),
        migrations.AlterField(
            model_name='home',
            name='square_meters',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
