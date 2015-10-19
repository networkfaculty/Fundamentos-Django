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

    publicada_recientemente.admin_order_field = 'fe_publicacion'
    publicada_recientemente.boolean = True
    publicada_recientemente.short_description = '¿Publicada recientemente?'

    class Meta:
        ordering = ['-fe_publicacion']

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    texto_opcion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_opcion

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
