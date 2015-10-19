from django.db import models
from django.utils import timezone
import datetime

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)
    fe_publicacion = models.DateTimeField('Fecha de Publicación')

    def __str__(self):
        return self.texto_pregunta

    def publicada_recientemente(self, dias=1):
        return self.fe_publicacion >= timezone.now() - datetime.timedelta(days=dias)

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    texto_opcion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_opcion
