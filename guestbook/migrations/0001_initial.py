# Generated by Django 3.2 on 2021-04-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guestbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45)),
                ('message', models.TextField()),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
