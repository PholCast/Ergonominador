# Generated by Django 5.1.2 on 2024-10-30 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mqttApp', '0005_postura'),
    ]

    operations = [
        migrations.AddField(
            model_name='postura',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]
