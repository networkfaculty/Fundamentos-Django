from django.shortcuts import render

from django.http import HttpResponse

#def index(request):
    #return HttpResponse("Este es el listado de encuestas")

from .models import Pregunta

#def index(request):
    #preguntas_recientes = Pregunta.objects.order_by('-fe_publicacion')[:5]
    #output = ', '.join([p.texto_pregunta for p in preguntas_recientes])
    #return HttpResponse(output)

#from django.template import RequestContext, loader

#def index(request):
    #preguntas_recientes = Pregunta.objects.order_by('-fe_publicacion')[:5]
    #template = loader.get_template('encuestas/index.html')
    #context = RequestContext(request, {
        #'preguntas_recientes': preguntas_recientes,
    #})
    #return HttpResponse(template.render(context))

def index(request):
    preguntas_recientes = Pregunta.objects.order_by('-fe_publicacion')[:5]
    context = { 'preguntas_recientes': preguntas_recientes }
    return render(request, 'encuestas/index.html', context)
