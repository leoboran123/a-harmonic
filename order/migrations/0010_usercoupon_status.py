# Generated by Django 4.1.5 on 2024-03-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_remove_coupon_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoupon',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='True', max_length=10),
        ),
    ]
