from django.conf.urls import url
from . import views

urlpatterns = [
    # ej: /encuestas/
    url(r'^$', views.index, name='index'),
    # ej: /encuestas/5
    url(r'^(?P<id_pregunta>\d+)/$', views.detalle, name='detalle'),
    # ej: /encuestas/5/resultados
    url(r'^(?P<id_pregunta>\d+)/resultados$', views.en_construccion, name='resultados'),
    # ej: /encuestas/5/votar
    url(r'^(?P<id_pregunta>\d+)/votar$', views.en_construccion, name='votar'),
]
