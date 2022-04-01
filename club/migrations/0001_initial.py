# Generated by Django 2.1.7 on 2022-04-01 12:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, max_length=1000)),
                ('written_at', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('image_url', models.ImageField(blank=True, upload_to='')),
            ],
            options={
                'db_table': 'club',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_at', models.DateField(default=datetime.datetime.now)),
                ('finish_at', models.DateField(default=datetime.datetime.now)),
                ('content', models.TextField(blank=True, max_length=1000)),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.Club')),
            ],
            options={
                'db_table': 'schedule',
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, max_length=1000)),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.Club')),
            ],
            options={
                'db_table': 'Todo',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='club_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.Club'),
        ),
        migrations.AddField(
            model_name='article',
            name='member_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Member'),
        ),
    ]
