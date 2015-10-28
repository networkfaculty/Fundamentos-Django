from .models import Pregunta, Opcion

from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from django.contrib import messages

from django.core.mail import send_mail
from smtplib import SMTPException
from .forms import *

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin, GroupRequiredMixin

class VistaIndex(generic.ListView):
    template_name = 'encuestas/index.html'
    context_object_name = 'preguntas_recientes'

    def get_queryset(self):
        return Pregunta.objects.order_by('-fe_publicacion')[:5]

    def get_context_data(self, **kwargs):
        context = super(VistaIndex, self).get_context_data(**kwargs)
        context['titulo'] = 'Listado de Encuestas'
        return context

# Agregamos LoginRequiredMixin para indicar que esta vista requiere autenticación
class VistaDetalle(LoginRequiredMixin, generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/detalle.html'

# En el caso de una vista sencilla (método), podemos usar directamente el decorador login_required
@login_required
def votar(request, id_pregunta):
    pregunta = get_object_or_404( Pregunta, pk=id_pregunta )
    try:
        # Nos aseguramos de que el código de la opción recibida esté dentro de las
        # opciones registradas para la pregunta
        opcion_seleccionada = pregunta.opcion_set.get(pk=request.POST['opcion'])

        # Incrementamos la cantidad de votos para la opción seleccionada, pero desde la
        # base de datos directamente
        # opcion_seleccionada.votos += 1 # Esto puede generar problemas en transacciones
                                        # concurrentes
        opcion_seleccionada.votos = F('votos') + 1
        opcion_seleccionada.save()
        # Nota: Lo anterior también podría escribirse de forma compacta como:
        # opcion_seleccionada.update( votos = F('votos') + 1 )

        # Luego de guardar exitosamente, redireccionamos a página de resultados.
        # Utilizamos 'reverse' para obtener de manera reutilizable la URL de la vista a
        # la que queremos redirigir al usuario.
        messages.success(request, "Voto registrado. ¡Gracias por participar!")
        return HttpResponseRedirect(reverse('encuestas:resultados',
                                            kwargs={'pk': pregunta.id}))
    except (KeyError, Opcion.DoesNotExist):
        # En caso de un código incorrecto o faltante de opción, volver a mostrar el formulario
        messages.error(request, "Opción faltante o inválida")
        return render(request, 'encuestas/detalle.html', {
            'pregunta': pregunta,
        })

class VistaResultados(generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/resultados.html'

def contacto(request):
    if request.method == 'POST':
        # Si ya se enviaron datos, se crea una instancia del formulario con ellos
        form = FormContacto(request.POST)
        # Y luego verificamos si es válido
        if form.is_valid():
            try:
                asunto = form.cleaned_data['asunto']
                mensaje = form.cleaned_data['mensaje']
                remitente = form.cleaned_data['remitente']
                cc_remitente = form.cleaned_data['cc_remitente']

                destinatarios = ['homero@example.com']
                if cc_remitente:
                    destinatarios.append(remitente)

                send_mail(asunto, mensaje, remitente, destinatarios)
                messages.success(request, 'Mensaje enviado')
                return HttpResponseRedirect( reverse('encuestas:index') )
            except (ConnectionRefusedError, SMTPException):
                messages.error(request, 'No se pudo enviar el mensaje')

    # Si no se enviaron datos, mostramos el formulario vacío
    else:
        form = FormContacto()

    return render(request, 'encuestas/contacto.html', {'form': form})

# Para las vistas de crear y editar preguntas y opciones, utilizaremos GroupRequiredMixin

class VistaCrearPregunta(GroupRequiredMixin, CreateView):
    model = Pregunta
    form_class = FormPregunta
    template_name = 'encuestas/agregar_pregunta.html'
    success_url = reverse_lazy('encuestas:index')
    group_required = 'puede_administrar_encuestas'

class VistaEditarPregunta(GroupRequiredMixin, UpdateView):
    model = Pregunta
    form_class = FormPregunta
    template_name = 'encuestas/editar_pregunta.html'
    success_url = reverse_lazy('encuestas:index')
    group_required = 'puede_administrar_encuestas'

class VistaOpciones(GroupRequiredMixin, UpdateView):
    '''
    En este ejemplo utilizamos un Formset personalizado para editar las opciones
    correspondientes a una pregunta. Por ello, utilizamos el modelo "padre" (Pregunta),
    y personalizamos los métodos get/post para obtener y guardar la lista de opciones
    '''
    model = Pregunta
    form_class = FormPregunta
    template_name = 'encuestas/editar_opciones.html'
    success_url = reverse_lazy('encuestas:index')
    group_required = 'puede_administrar_encuestas'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        opciones_form = FormPreguntaOpciones(instance=self.object)
        return self.render_to_response(
            self.get_context_data(opciones_form=opciones_form,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        opciones_form = FormPreguntaOpciones(request.POST, instance=self.object)
        if opciones_form.is_valid():
            opciones_form.save()
            messages.success(request, 'Opciones guardadas')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'No se pudieron guardar las opciones')
            return self.render_to_response(
                self.get_context_data(opciones_form=opciones_form,))
