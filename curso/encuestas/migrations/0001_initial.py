# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('texto_opcion', models.CharField(max_length=200)),
                ('votos', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('texto_pregunta', models.CharField(max_length=200)),
                ('fe_publicacion', models.DateTimeField(verbose_name='Fecha de Publicación')),
            ],
        ),
        migrations.AddField(
            model_name='opcion',
            name='pregunta',
            field=models.ForeignKey(to='encuestas.Pregunta'),
        ),
    ]
