# Generated by Django 4.0.4 on 2022-04-29 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_customers_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=20000, verbose_name='Shop Name')),
                ('shop_details', models.TextField(verbose_name='Shop Details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopholder', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
