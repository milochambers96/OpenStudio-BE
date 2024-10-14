# Generated by Django 5.1.1 on 2024-10-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('ready to ship', 'Ready to Ship'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=30),
        ),
    ]
