# Generated by Django 3.2.9 on 2021-12-06 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(null=True)),
                ('end', models.DateField(null=True)),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calculation.candidate')),
            ],
        ),
    ]
