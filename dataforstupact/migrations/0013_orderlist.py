# Generated by Django 4.0.6 on 2022-07-08 17:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0012_alter_stumartmodel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderlist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('buyer', models.CharField(max_length=30)),
                ('region', models.CharField(max_length=40)),
            ],
        ),
    ]
