# Generated by Django 4.1.3 on 2022-11-15 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unepccc_app', '0003_status_type_pdd_consultant_buyer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Validator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('short_name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.country')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.type')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('project_id', models.CharField(max_length=50)),
                ('project_idVal', models.CharField(max_length=100)),
                ('project_ref', models.CharField(max_length=20)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.buyer')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.country')),
                ('methodology', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.methodology')),
                ('pdd_consultant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.pdd_consultant')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.status')),
                ('sub_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.sub_type')),
                ('validator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.validator')),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unepccc_app.project')),
            ],
        ),
    ]
