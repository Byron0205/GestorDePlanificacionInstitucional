from django import forms
from .models import Departamento

class AgregarSolicitud(forms.Form):
    titulo = forms.CharField(required=True, min_length=4, max_length=30,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'titulo',
        'placeholder': 'Titulo'
    }))
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(),required=True, widget=forms.Select(attrs={
        'class': 'form-control',
        'id': 'dpto',
        'placeholder': 'Departamento'
    }))
    fechaLimite = forms.DateField(required=True,label='Fecha Limite', widget=forms.DateInput(format='%d/%m/%Y',attrs={
        'type': 'date',
        'class': 'form-control',
        "id": 'fecha-limite'
        }))
    detalle = forms.CharField(label='Detalle',widget=forms.Textarea(attrs={
        'rows': '3',
        'class': 'form-control',
        'id': 'descripcion'
        }))
    etapa = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'etapa'
    }))
