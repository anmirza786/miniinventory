# Generated by Django 4.0.4 on 2022-05-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_customers_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Customer`s Credit Fee'),
        ),
    ]