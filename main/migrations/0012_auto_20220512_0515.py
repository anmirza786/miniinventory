# Generated by Django 3.2.8 on 2022-05-12 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_fee_month'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fee',
            name='Month',
        ),
        migrations.AlterField(
            model_name='customers',
            name='customer_status',
            field=models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled')], default='disabled', max_length=10),
        ),
    ]
