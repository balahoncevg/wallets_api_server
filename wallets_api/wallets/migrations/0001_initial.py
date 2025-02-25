# Generated by Django 3.2.25 on 2025-02-25 14:09

from decimal import Decimal
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
            ],
        ),
    ]
