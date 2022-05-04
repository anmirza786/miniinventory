# Generated by Django 4.0.4 on 2022-05-02 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_alter_fee_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subuser',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
