# Generated by Django 3.1a1 on 2020-06-17 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='apple_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
