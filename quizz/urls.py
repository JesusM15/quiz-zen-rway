from django.urls import path
from . import views


urlpatterns = [
    path('', views.quizList, name='home'),
    path('busqueda?=', views.quizListSearch, name='search_list'),
    path('quiz/<int:quiz_id>/<slug:quiz_slug>/', views.quiz, name='quiz'),
    path('quiz/resultados/<slug:quiz_slug>/', views.rank, name='rank'),
    path('quiz/resultados/<slug:quiz_slug>/1357810233673246890354629<puntos>32809246314311976423/', views.rank, name='rank'),
    path('quiz/procesando-resultados/<slug:quiz_slug>/', views.calificador, name='calificador'),
    
    path('quiz/crear-quiz/de/<usuario>/', views.createQuiz, name='create_quiz'),
    path('quiz/editar-quiz/<usuario>/<slug:quiz_slug>/', views.editQuiz, name='edit_quiz'),
    path('quiz/crear-preguntas/<usuario>/<slug:quiz_slug>/', views.createQuestions, name='create_questions'),
    path('quiz/crear-opciones/<usuario>/<slug:quiz_slug>/<int:pregunta_id>/', views.createAnswers, name='create_answers'),
    path('quiz/editar-pregunta/<usuario>/<slug:quiz_slug>/<int:pregunta_id>/', views.editPregunta, name='edit_pregunta'),
    path('quiz/eliminar-preguntas/<usuario>/<slug:quiz_slug>/<int:pregunta_id>/', views.deleteQuestions, name='delete_questions'),
    path('quiz/eliminar-opciones/<usuario>/<slug:quiz_slug>/<int:pregunta_id>/<int:answer_id>/', views.deleteAnswers, name='delete_answers'),
    path('quiz/eliminar/<usuario>/<int:quiz_id>/', views.deleteQuiz, name='delete_quiz'),
    path('quiz/editar-opcion/<usuario>/<slug:quiz_slug>/<int:pregunta_id>/<int:answer_id>/', views.editAnswer, name='edit_answer'),    

    
]