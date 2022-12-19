from django import forms
from .models import *

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['nombre', 'imagen', 'aprobado', 'tag']
        
class EditarQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['nombre', 'imagen', 'aprobado']
        
class CrearPregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'imagen', 'puntos']

class CrearRespuesta(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['cuerpo', 'correcta']

class EditarPregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'imagen', 'puntos']
        
class EditarRespuesta(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['cuerpo', 'correcta']
