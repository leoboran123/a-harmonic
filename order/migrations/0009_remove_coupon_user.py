# Generated by Django 4.1.5 on 2024-03-13 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_usercoupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
    ]
