# Generated by Django 4.1.5 on 2024-03-13 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_coupon_create_at_alter_coupon_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=30),
        ),
    ]