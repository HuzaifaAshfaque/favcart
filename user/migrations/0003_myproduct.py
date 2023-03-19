# Generated by Django 3.2.4 on 2022-09-03 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='myproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pprice', models.FloatField()),
                ('dprice', models.FloatField()),
                ('psize', models.CharField(max_length=20)),
                ('pcolor', models.CharField(max_length=20)),
                ('pdes', models.TextField()),
                ('pdel', models.CharField(max_length=60)),
                ('ppic', models.ImageField(default='', upload_to='static/product/')),
                ('pdate', models.DateField()),
                ('pcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.category')),
            ],
        ),
    ]
