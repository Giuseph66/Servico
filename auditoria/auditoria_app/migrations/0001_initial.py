# Generated by Django 5.1.2 on 2024-10-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField(max_length=255)),
                ('cell', models.IntegerField()),
                ('gmail', models.EmailField(max_length=500)),
                ('senha', models.CharField(max_length=100)),
            ],
        ),
    ]
