from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import *
from .forms import *
from django.contrib.auth.hashers import check_password

def quizList(request):
    
    quiz_list = Quiz.objects.all().filter(aprobado=True)
    #paginacion con 9 post
    paginator = Paginator(quiz_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        quizzes = paginator.page(page_number)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)
        
    context = {'quizzes':quizzes, 'bus': True}
    return render(request, 'quiz/list.html', context)

def quizListSearch(request):
    
    search = request.GET.get('query')
    
    quiz_list = Quiz.objects.all().filter(aprobado=True, nombre__contains=search)
    #paginacion con 9 post
    paginator = Paginator(quiz_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        quizzes = paginator.page(page_number)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)
        
    context = {'quizzes':quizzes, 'bus': True}
    return render(request, 'quiz/list.html', context)

@login_required
def quiz(request, quiz_id, quiz_slug):
    
    quiz = get_object_or_404(Quiz, id=quiz_id, slug=quiz_slug)
    preguntas = quiz.preguntas.all()
    
    context = {'preguntas':preguntas, 'quiz': quiz}
    
    return render(request, 'quiz/quiz.html', context)
    

@login_required
@require_POST
def calificador(request, quiz_slug):
    
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    puntos = 0
        
    for i in range(1,quiz.preguntas.all().count()+1):
        ans = str(request.POST.get('respuesta'+str(i)))
        rightAns = str(quiz.preguntas.all()[i-1].opciones.get(correcta=True))
        if ans == rightAns:puntos+= quiz.preguntas.all()[i-1].puntos
        
    try:
        puntuacion = get_object_or_404(Ponderacion, quiz=quiz, usuario=request.user)
        if puntuacion.puntos < puntos:
            puntuacion.puntos = puntos
            puntuacion.save()
    except:
        puntuacion = Ponderacion(usuario=request.user, quiz=quiz, puntos=puntos)
        #guardar puntuacion en la base de datos
        puntuacion.save()
    
    return redirect(reverse('rank', args=[quiz.slug, puntos]))

       
def rank(request, quiz_slug, puntos=None):
    puntuacion=None
    maxpuntos= 0
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    topPlayers = quiz.puntuaciones.all().order_by('-puntos')[:5]
    
    if request.user.user_puntuacion: puntuacion = get_object_or_404(Ponderacion, usuario=request.user, quiz=quiz)
    
    for pregunta in quiz.preguntas.all():maxpuntos += pregunta.puntos
            
    context = {'puntuacion':puntuacion, 'quiz': quiz, 'maxpuntos':maxpuntos, 'topPlayers': topPlayers, 'currentPuntos': puntos,}        
    
    return render(request, 'quiz/results.html', context)
    

@login_required
def createQuiz(request, usuario):
    
    user = get_object_or_404(User, username=usuario)
    quiz = None
    
    if request.method == 'POST':
        quiz_form = QuizForm(data=request.POST, files=request.FILES)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.autor = request.user
            quiz.save()
            return redirect(reverse('create_questions', args=[quiz.autor, quiz.slug]))
    else:
        quiz_form = QuizForm()
    
    context = {'user':user, 'quiz_form': quiz_form}
    
    return render(request, 'quiz/create.html', context)

@login_required
def editQuiz(request, usuario, quiz_slug):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, slug=quiz_slug, autor=user)
    
    if request.method == 'POST':
        quiz_form = EditarQuizForm(instance=quiz, data=request.POST, files=request.FILES)
        if quiz_form.is_valid():
            quiz_form.save()
            return redirect(reverse('ver_perfil', args=[quiz.autor]))
    else:
        quiz_form = EditarQuizForm(instance=quiz)   
        
    return render(request, 'quiz/edit_quiz.html', {'quiz_form': quiz_form, 'quiz':quiz}) 


@login_required
def createQuestions(request, usuario, quiz_slug):
            
    user = get_object_or_404(User, username=usuario)
    
    quiz = get_object_or_404(Quiz, autor=user, slug=quiz_slug)
    
    preguntas = Pregunta.objects.filter(quiz=quiz).order_by('-creado')
        
    if request.method == 'POST':
        form_p = CrearPregunta(data=request.POST, files=request.FILES)
        if form_p.is_valid():
            pregunta = form_p.save(commit=False)
            pregunta.quiz = quiz
            pregunta.save()
            return redirect(reverse('create_questions', args=[request.user.username, quiz.slug]))
    else:
        form_p = CrearPregunta()

    
    context = {'quiz':quiz, 'user':user, 'form_p': form_p, 'preguntas':preguntas,}
    
    return render(request, 'quiz/create_questions.html', context)

@login_required
def editPregunta(request, usuario, quiz_slug, pregunta_id):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, autor=user, slug=quiz_slug)
    pregunta = get_object_or_404(Pregunta, quiz=quiz, pk=pregunta_id)
    
    if request.user != quiz.autor:return redirect('home')
    
    if request.method == 'POST':
        edit_form = EditarPregunta(instance=pregunta, data=request.POST, files=request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('create_questions', args=[request.user.username, quiz.slug]))
    else:
        edit_form = EditarPregunta(instance=pregunta)
    
    context = {'edit_form': edit_form, 'pregunta':pregunta}
    
    return render(request, 'quiz/edit_question.html', context)
    

@login_required
def deleteQuestions(request, usuario, quiz_slug, pregunta_id):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, autor=user, slug=quiz_slug)
    pregunta = get_object_or_404(Pregunta, quiz=quiz, pk=pregunta_id)
    
    if request.user == quiz.autor:
        pregunta.delete()
    
    return redirect(reverse('create_questions', args=[request.user.username, quiz.slug]))
    
@login_required
def createAnswers(request, usuario, quiz_slug, pregunta_id):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, autor=user, slug=quiz_slug)
    pregunta = get_object_or_404(Pregunta, quiz=quiz, pk=pregunta_id)
    opciones = Opcion.objects.filter(pregunta=pregunta)
    
    if request.method == 'POST':
        form_r = CrearRespuesta(request.POST)
        if form_r.is_valid():
            respuesta = form_r.save(commit=False)
            respuesta.pregunta = pregunta
            respuesta.save()
            return redirect(reverse('create_answers', args=[request.user.username, quiz.slug, pregunta.id]))
    else:
        form_r = CrearRespuesta()
    
    context = {'user':user, 'quiz':quiz, 'pregunta':pregunta, 'opciones': opciones,'form_r':form_r,}
    
    return render(request, 'quiz/create_answers.html', context)

@login_required
def editAnswer(request, usuario, quiz_slug, pregunta_id, answer_id):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, autor=user, slug=quiz_slug)
    pregunta = get_object_or_404(Pregunta, quiz=quiz, pk=pregunta_id)
    respuesta = get_object_or_404(Opcion, pregunta=pregunta, pk=answer_id)
    
    if request.user != quiz.autor:return redirect('home')
    if request.method == 'POST':
        form_r = EditarRespuesta(instance=respuesta, data=request.POST)
        if form_r.is_valid():
            form_r.save()
            return redirect(reverse('create_answers', args=[request.user.username, quiz.slug, pregunta.id]))
    else:
        form_r = EditarRespuesta(instance=respuesta)
        
    context = {'respuesta': respuesta, 'form_r': form_r}
    return render(request, 'quiz/edit_answer.html', context)
    
@login_required
def deleteAnswers(request, usuario, quiz_slug, pregunta_id, answer_id):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, autor=user, slug=quiz_slug)
    pregunta = get_object_or_404(Pregunta, quiz=quiz, pk=pregunta_id)
    respuesta = get_object_or_404(Opcion, pregunta=pregunta, pk=answer_id)
    
    if request.user == quiz.autor:
        respuesta.delete()
    
    return redirect(reverse('create_answers', args=[request.user.username, quiz.slug, pregunta.id]))


@login_required
def deleteQuiz(request, usuario, quiz_id):
    user = get_object_or_404(User, username=usuario)
    quiz = get_object_or_404(Quiz, autor=user, pk=quiz_id)
    if request.user == quiz.autor:
        quiz.delete()
    
    return redirect(reverse('ver_perfil', args=[request.user.username]))

