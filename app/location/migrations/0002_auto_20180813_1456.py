# Generated by Django 2.1 on 2018-08-13 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pensionlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pensionimage',
            name='pension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pensionimages', to='location.Pension'),
        ),
        migrations.AddField(
            model_name='pension',
            name='sub_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pensions', to='location.SubLocation'),
        ),
    ]
