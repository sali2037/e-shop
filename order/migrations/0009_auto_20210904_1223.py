# Generated by Django 3.2.5 on 2021-09-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_numer',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
