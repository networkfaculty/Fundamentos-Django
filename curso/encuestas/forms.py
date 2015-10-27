from django import forms
from .models import Pregunta, Opcion
from bootstrap3_datetime.widgets import DateTimePicker
from django.forms.models import inlineformset_factory

class FormContacto(forms.Form):
    asunto = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)
    remitente = forms.EmailField()
    cc_remitente = forms.BooleanField(label='Envíame una copia', required=False)

class FormPregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto_pregunta','fe_publicacion']
        widgets = {'texto_pregunta': forms.Textarea(attrs={'rows':3}),
                   'fe_publicacion': DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False})}

FormPreguntaOpciones = inlineformset_factory(
    Pregunta,
    Opcion,
    fields = ('texto_opcion',),
    max_num = 5,
    extra = 5,
)