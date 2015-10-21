from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from .models import Pregunta
from django.http import Http404

def index(request):
    preguntas_recientes = Pregunta.objects.order_by('-fe_publicacion')[:5]
    context = { 'preguntas_recientes': preguntas_recientes }
    return render(request, 'encuestas/index.html', context)

#def detalle(request, id_pregunta):
    #try:
        #pregunta = Pregunta.objects.get(pk=id_pregunta)
    #except Pregunta.DoesNotExist:
        #raise Http404('La pregunta no fue encontrada')
    #return render(request, 'encuestas/detalle.html', {'pregunta': pregunta})

def detalle(request, id_pregunta):
    pregunta = get_object_or_404( Pregunta, pk=id_pregunta )
    return render(request, 'encuestas/detalle.html', {'pregunta': pregunta})

def en_construccion(request, id_pregunta):
    return HttpResponse('Página '+ request.resolver_match.view_name +
                        ' en construcción para #'+str(id_pregunta))