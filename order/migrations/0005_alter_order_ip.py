# Generated by Django 3.2.5 on 2021-09-02 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_order_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]