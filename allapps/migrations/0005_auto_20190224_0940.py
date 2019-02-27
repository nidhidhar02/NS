# Generated by Django 2.1.7 on 2019-02-24 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allapps', '0004_pincode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='id',
        ),
        migrations.AlterField(
            model_name='cart',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order_status',
            field=models.CharField(default='Nothing', max_length=30),
        ),
        migrations.AlterField(
            model_name='pincode',
            name='pincode',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
