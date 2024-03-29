# Generated by Django 4.0.6 on 2022-07-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0023_alter_notifications_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_list',
            name='delivery_charge',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='order_list',
            name='price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='time',
            field=models.CharField(default='20220711064614', max_length=20),
        ),
    ]
