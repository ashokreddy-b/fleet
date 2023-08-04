# Generated by Django 4.2.1 on 2023-07-06 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FleetManagerData',
            fields=[
                ('manager_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('manager_name', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('contact_no', models.TextField()),
                ('email', models.CharField(max_length=20)),
                ('organisation', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'fleet_manager_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ManagerSignup',
            fields=[
                ('id', models.CharField()),
                ('manager_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='fleetapi.fleetmanagerdata')),
                ('fullname', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=25)),
                ('password', models.TextField()),
            ],
            options={
                'db_table': 'manager_signup',
                'managed': False,
            },
        ),
    ]
