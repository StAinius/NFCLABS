# Generated by Django 5.2 on 2025-05-27 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NFCLabs', '0007_alter_contactpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='form_type',
            field=models.CharField(choices=[('contact', 'Contact Form'), ('partner', 'Partner Form'), ('quote', 'Quote Form')], default='contact', max_length=20),
        ),
    ]
