from django.contrib import admin

from .models import Pregunta, Opcion
from django.forms import Textarea
from django.db import models
from django.contrib.admin import AdminSite

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3

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
    inlines = [OpcionInline]
    list_display = [ 'texto_pregunta', 'fe_publicacion', 'publicada_recientemente' ]
    list_filter = [ 'fe_publicacion' ]
    search_fields = ['texto_pregunta']

class SitioAdministrativo(AdminSite):
    site_header = 'Sitio Administrativo Personalizado'

admin_site = SitioAdministrativo(name='curso-admin')

admin_site.register(Pregunta, PreguntaAdmin)
