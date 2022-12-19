from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'autor', 'creado']
    prepopulated_fields = {'slug':('nombre',)}
    list_filter = ['creado', 'tag', 'autor']
    
@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'puntos', 'creado']
    list_filter = ['creado', 'puntos']
    
@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ['cuerpo', 'pregunta', 'correcta']
    list_filter = ['creado', 'correcta', 'pregunta']
    
@admin.register(Ponderacion)
class PonderacionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'puntos']
    list_filter = ['usuario', 'quiz']

