# Generated by Django 5.1.4 on 2024-12-06 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
