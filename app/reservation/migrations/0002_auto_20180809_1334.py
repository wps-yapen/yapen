# Generated by Django 2.0.7 on 2018-08-09 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checkin_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='checkout_date',
            field=models.DateField(blank=True),
        ),
    ]
