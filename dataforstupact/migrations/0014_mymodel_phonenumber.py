# Generated by Django 4.0.6 on 2022-07-08 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0013_orderlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]