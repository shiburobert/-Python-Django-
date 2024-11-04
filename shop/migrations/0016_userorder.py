# Generated by Django 5.1 on 2024-10-02 09:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_delete_userorder'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_qty', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('shipping_address', models.TextField()),
                ('payment_method', models.CharField(max_length=50)),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending', max_length=50)),
                ('expected_delivery', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]