# Generated by Django 4.2.2 on 2023-07-02 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('department', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='attendant',
            name='created_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='attendant',
            name='modified_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientmaster',
            name='created_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientmaster',
            name='modified_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='voucher',
            name='created_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='voucher',
            name='modified_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 2, 14, 8, 42, 752998, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='clientmaster',
            name='active_vouchers',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='clientmaster',
            name='last_order_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clientmaster',
            name='used_vouchers',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='txn_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 2, 14, 8, 42, 751999, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='last_used',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 2, 14, 8, 42, 751999, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
