# Generated by Django 4.0.5 on 2022-06-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataforstupact', '0007_alter_mymodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='image',
            field=models.ImageField(blank=True, default='user.png', upload_to=''),
        ),
    ]
