# Generated by Django 4.0.6 on 2022-07-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0026_order_list_title_alter_notifications_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='time',
            field=models.CharField(default='20220711115028', max_length=20),
        ),
    ]
