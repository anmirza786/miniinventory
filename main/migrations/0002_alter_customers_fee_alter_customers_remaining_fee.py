# Generated by Django 4.0.4 on 2022-04-17 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Customer`s Paid Fee'),
        ),
        migrations.AlterField(
            model_name='customers',
            name='remaining_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Customer`s Remaining Fee'),
        ),
    ]