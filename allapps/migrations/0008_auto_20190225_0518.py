# Generated by Django 2.1.7 on 2019-02-25 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allapps', '0007_auto_20190225_0423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emidetails',
            old_name='total_bill_amount',
            new_name='emi_value',
        ),
    ]
