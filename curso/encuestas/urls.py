from django.conf.urls import url
from . import views

urlpatterns = [
    # ej: /encuestas/
    url(r'^$', views.VistaIndex.as_view(), name='index'),
    # ej: /encuestas/5
    # Las vistas detalladas genéricas esperan que el argumento se llame 'pk'
    url(r'^(?P<pk>\d+)/$', views.VistaDetalle.as_view(), name='detalle'),
    # ej: /encuestas/5/resultados
    url(r'^(?P<pk>\d+)/resultados$', views.VistaResultados.as_view(), name='resultados'),
    # ej: /encuestas/5/votar
    url(r'^(?P<id_pregunta>\d+)/votar$', views.votar, name='votar'),
    url(r'^contacto$', views.contacto, name='contacto'),
]
