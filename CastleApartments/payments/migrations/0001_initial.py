# Generated by Django 5.2 on 2025-05-11 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('real_estates', '0007_alter_property_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_option', models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('BANK_ACCOUNT', 'Bank Account'), ('MORTGAGE', 'Mortgage')], max_length=16)),
                ('payment_time', models.DateTimeField(auto_now_add=True)),
                ('offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='real_estates.offer')),
            ],
        ),
    ]
