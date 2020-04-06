# Generated by Django 3.0.3 on 2020-04-02 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transient_fields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_ID', models.CharField(default='', max_length=5, verbose_name='Field ID')),
                ('nights', models.CharField(default='', max_length=100, verbose_name='Dates of nights with matching pairs')),
                ('number', models.IntegerField(default='', verbose_name='Number of matching pairs')),
            ],
            options={
                'ordering': ['field_ID'],
            },
        ),
        migrations.CreateModel(
            name='Transient_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_1', models.CharField(default='', max_length=100, verbose_name='File 1')),
                ('file_2', models.CharField(default='', max_length=100, verbose_name='File 2')),
                ('filter_1', models.CharField(default='', max_length=1, verbose_name='Filter 1')),
                ('filter_2', models.CharField(default='', max_length=1, verbose_name='Filter 2')),
                ('scorr_1', models.CharField(max_length=10, null=True, verbose_name='Scorr 1')),
                ('scorr_2', models.CharField(max_length=10, null=True, verbose_name='Scorr 2')),
                ('mag_1', models.CharField(max_length=10, null=True, verbose_name='Mag 1')),
                ('mag_2', models.CharField(max_length=10, null=True, verbose_name='Mag 2')),
                ('dt_1', models.CharField(max_length=10, null=True, verbose_name='Δt_1 (days)')),
                ('dt_2', models.CharField(max_length=10, null=True, verbose_name='Δt_2 (days)')),
                ('date_observed', models.CharField(default='', max_length=2, verbose_name='Date-observed')),
                ('coords', models.CharField(default='', max_length=50, verbose_name='Coordinates (degrees)')),
                ('img', models.ImageField(blank=True, null=True, upload_to='vetting/')),
                ('field_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vetting.Transient_fields')),
            ],
        ),
    ]
