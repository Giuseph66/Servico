# Generated by Django 5.1.2 on 2024-11-05 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria_app', '0002_precosse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conexao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=50)),
                ('hostname', models.CharField(default='Nao cadastrado', max_length=255)),
                ('user_agent', models.TextField()),
                ('referer', models.CharField(default='Direct Access', max_length=255)),
                ('language', models.CharField(default='Mudinho', max_length=255)),
                ('session_id', models.CharField(max_length=50, unique=True)),
                ('host', models.CharField(default='impossivel', max_length=255)),
                ('connection_type', models.CharField(default='limpo', max_length=50)),
                ('data_conexao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
