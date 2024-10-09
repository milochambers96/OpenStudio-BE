# Generated by Django 5.1.1 on 2024-10-09 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artwork_images', '0001_initial'),
        ('artworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artworkimage',
            name='artwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks_images', to='artworks.artwork'),
        ),
    ]
