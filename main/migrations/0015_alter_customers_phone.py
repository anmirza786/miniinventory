# Generated by Django 3.2.8 on 2022-05-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20220512_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Customer`s Phone Number'),
        ),
    ]