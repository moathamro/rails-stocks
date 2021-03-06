# Generated by Django 3.1.2 on 2020-11-24 11:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=300)),
                ('year', models.CharField(choices=[('1', '20'), ('2', '22'), ('3', '23'), ('4', '24'), ('5', '25')], max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_price', models.FloatField(null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 11, 24, 13, 17, 32, 305184))),
                ('shares', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('symbol', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('change_over_time', models.FloatField(null=True)),
                ('top_rank', models.IntegerField(null=True)),
                ('price', models.FloatField(null=True)),
                ('change', models.FloatField(null=True)),
                ('change_percent', models.FloatField(null=True)),
                ('market_cap', models.FloatField(null=True)),
                ('primary_exchange', models.CharField(max_length=32, null=True)),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(related_name='fav_set', to=settings.AUTH_USER_MODEL)),
                ('portfolio_list', models.ManyToManyField(related_name='port_set', through='myapp.Portfolio', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth', models.CharField(blank=True, default='', max_length=100)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('job', models.CharField(blank=True, default='', max_length=300)),
                ('bio', models.CharField(blank=True, default='', max_length=300)),
                ('website', models.URLField(blank=True, default='')),
                ('image', models.ImageField(blank=True, default='profile.png', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='portfolio',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.stock'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_raise', models.FloatField(null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 11, 24, 11, 17, 32, 305184, tzinfo=utc))),
                ('notifications', models.ManyToManyField(related_name='notifications_set', to=settings.AUTH_USER_MODEL)),
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=100)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 11, 24, 13, 17, 32, 305184))),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='portfolio',
            unique_together={('user', 'stock')},
        ),
    ]
