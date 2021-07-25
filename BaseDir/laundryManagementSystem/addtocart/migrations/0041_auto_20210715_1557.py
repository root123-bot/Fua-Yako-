# Generated by Django 3.0 on 2021-07-15 15:57

import datetime
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('addtocart', '0040_auto_20210715_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='arrived_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 15, 15, 57, 20, 277761), null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 17, 15, 57, 20, 276160), null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='items',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
