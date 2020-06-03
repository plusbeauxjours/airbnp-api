# Generated by Django 3.1a1 on 2020-06-03 06:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200603_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
