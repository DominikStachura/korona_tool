# Generated by Django 2.2.1 on 2020-03-29 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200326_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions_all', models.CharField(blank=True, max_length=1000, null=True)),
                ('answers_all', models.CharField(blank=True, max_length=1000, null=True)),
                ('code', models.CharField(max_length=8)),
            ],
        ),
    ]
