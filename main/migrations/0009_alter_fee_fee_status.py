# Generated by Django 3.2.8 on 2022-05-11 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_fee_fee_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='fee_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('not_paid', 'Not Paid')], default='not_paid', max_length=10),
        ),
    ]
