# Generated by Django 5.2 on 2025-05-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_content', '0002_alter_pagecontent_options_alter_pagecontent_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagecontent',
            name='title',
            field=models.TextField(verbose_name='Name'),
        ),
    ]
