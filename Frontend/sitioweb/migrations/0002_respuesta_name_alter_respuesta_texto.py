# Generated by Django 4.0.4 on 2022-05-02 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitioweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='name',
            field=models.TextField(default='SOME STRING', max_length=140),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='texto',
            field=models.TextField(default='SOME STRING'),
        ),
    ]
