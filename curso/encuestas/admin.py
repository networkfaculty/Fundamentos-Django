from django.contrib import admin

from .models import Pregunta
from django.forms import Textarea
from django.db import models

#class PreguntaAdmin(admin.ModelAdmin):
    #fields = ['fe_publicacion', 'texto_pregunta']

#class PreguntaAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, { 'fields': [ 'texto_pregunta' ] }),
        #('Información adicional', { 'fields': [ 'fe_publicacion' ] } )
    #]

class PreguntaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'style':'width:90%', 'rows':5})},
    }
    fieldsets = [
        (None, { 'fields': [ 'texto_pregunta' ] }),
        ('Información adicional', {
            'fields': [ 'fe_publicacion' ],
            'classes': [ 'collapse' ]
            }
        ),
    ]

admin.site.register(Pregunta, PreguntaAdmin)