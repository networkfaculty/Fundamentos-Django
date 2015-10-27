from django import forms

class FormContacto(forms.Form):
    asunto = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)
    remitente = forms.EmailField()
    cc_remitente = forms.BooleanField(label='Envíame una copia', required=False)
