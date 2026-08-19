from django import forms
from .models import Proyecto, Tarea, Subtarea


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'fecha_limite', 'etiquetas']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'etiquetas': forms.CheckboxSelectMultiple(),
        }


class SubtareaForm(forms.ModelForm):
    class Meta:
        model = Subtarea
        fields = ['texto']
        widgets = {'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nueva subtarea...'})}