from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
#tag = TaggableManager()
# Create your models here.

class Quiz(models.Model):
    
    nombre = models.CharField(max_length=140)
    slug = models.SlugField(max_length=200, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='quizz/portada/%Y/%m/%d')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    aprobado = models.BooleanField(default=True)
    tag = TaggableManager()
    
    class Meta:
        ordering = ['-creado']
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('quiz', args=[self.id, self.slug])

class Pregunta(models.Model):
    titulo = models.CharField(max_length=160)
    imagen = models.ImageField(upload_to='preguntas/images/%Y/%m/%d', blank=True)
    puntos = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='preguntas')
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['creado']

    def __str__(self):
        return self.titulo

class Opcion(models.Model):
    cuerpo = models.CharField(max_length=300)
    creado = models.DateTimeField(auto_now_add=True)
    correcta = models.BooleanField(default=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    
    class Meta:
        verbose_name = 'Opcion'
        verbose_name_plural = 'Opciones'
        ordering = ['creado']
        
    def __str__(self):
        return f'{self.cuerpo}'

    
class Ponderacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_puntuacion')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='puntuaciones')
    puntos = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return f'Puntuacion de {self.usuario}'