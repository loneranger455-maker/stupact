# Generated by Django 4.0.6 on 2022-07-08 13:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0010_stumartmodel_alter_mymodel_batch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stumartmodel',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=50, primary_key=True, serialize=False),
        ),
    ]
