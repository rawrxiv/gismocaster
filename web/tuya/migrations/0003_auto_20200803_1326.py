# Generated by Django 3.0.7 on 2020-08-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tuya", "0002_gismomodel_api_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gismomodel",
            name="api_model",
            field=models.CharField(blank=True, default="", max_length=32, null=True),
        ),
    ]
