# Generated by Django 4.0.6 on 2022-08-13 16:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0036_queries_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queries',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
