# Generated by Django 5.1.2 on 2024-11-22 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_product_selling_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='unit_price',
            new_name='cost_price',
        ),
    ]