# Generated by Django 3.2.4 on 2021-08-27 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DokumentasiKategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('max_request', models.IntegerField()),
                ('allow_ip', models.TextField()),
                ('max_ip', models.IntegerField()),
                ('harga', models.IntegerField()),
                ('expired', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.TextField()),
                ('email', models.TextField()),
                ('picture', models.TextField()),
                ('email_verfied', models.BooleanField()),
                ('verified_token', models.CharField(max_length=256)),
                ('password', models.TextField(max_length=256)),
                ('expired', models.DateTimeField()),
                ('apikey', models.CharField(max_length=256)),
                ('plan_name', models.TextField()),
                ('max_request', models.IntegerField()),
                ('allow_ip', models.TextField()),
                ('max_ip', models.IntegerField()),
                ('req_counter', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ua', models.CharField(max_length=256)),
                ('ip', models.CharField(max_length=50)),
                ('cookie_value', models.CharField(max_length=256)),
                ('AccessToken', models.CharField(max_length=256)),
                ('Action', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='Dokumentasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=50)),
                ('title_panel', models.CharField(max_length=100)),
                ('url_dokumentasi', models.CharField(max_length=30)),
                ('example_ajax', models.JSONField()),
                ('path_api', models.CharField(max_length=200)),
                ('categori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.dokumentasikategori')),
            ],
        ),
        migrations.CreateModel(
            name='CodeDocumentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=64)),
                ('language_code', models.CharField(max_length=50)),
                ('code', models.TextField()),
                ('api_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.dokumentasi')),
            ],
        ),
    ]
