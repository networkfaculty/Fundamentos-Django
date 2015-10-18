from django.db import models

# Create your models here.

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)
    fe_publicacion = models.DateTimeField('Fecha de Publicación')


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    texto_opcion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
