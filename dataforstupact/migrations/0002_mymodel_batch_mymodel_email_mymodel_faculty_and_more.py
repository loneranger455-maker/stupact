# Generated by Django 4.0.5 on 2022-06-29 04:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='batch',
            field=models.CharField(default=datetime.datetime(2022, 6, 29, 4, 51, 19, 366642, tzinfo=utc), max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mymodel',
            name='email',
            field=models.EmailField(default=datetime.datetime(2022, 6, 29, 4, 51, 40, 603337, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mymodel',
            name='faculty',
            field=models.CharField(default=datetime.datetime(2022, 6, 29, 4, 51, 55, 361865, tzinfo=utc), max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mymodel',
            name='first_name',
            field=models.CharField(default=datetime.datetime(2022, 6, 29, 4, 52, 0, 654076, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mymodel',
            name='last_name',
            field=models.CharField(default=datetime.datetime(2022, 6, 29, 4, 52, 5, 939450, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
    ]
