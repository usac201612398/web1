# Generated by Django 4.1 on 2024-01-05 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_mqttlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Código_Articulo', models.CharField(max_length=15)),
                ('Artículo', models.CharField(max_length=125)),
                ('Unidad_Medida', models.CharField(max_length=15)),
            ],
        ),
    ]
