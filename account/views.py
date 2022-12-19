from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from quizz.models import *
from django.urls import reverse
from django.views.decorators.http import require_POST
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

@login_required
def adminPerfil(request, username):
    
    user = get_object_or_404(User, username=username)
    
    profile = get_object_or_404(Profile, user=user)
    
    quiz_list = Quiz.objects.filter(autor=user)
    paginator = Paginator(quiz_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        quizzes = paginator.page(page_number)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)
    
    context = {'profile':profile,'user':user, 'quizzes':quizzes,}    
        
    return render(request, 'account/profile/admin.html', context)


def acercade(request):
    
    return render(request, 'info/help.html')


@login_required
def myranks(request, username):
    
    user = get_object_or_404(User, username=username)
    ponderaciones_list = user.user_puntuacion.all()
    
    paginator = Paginator(ponderaciones_list, 8)
    page_number = request.GET.get('page', 1)
    
    try:
        ponderaciones = paginator.page(page_number)
    except PageNotAnInteger:
        ponderaciones = paginator.page(1)
    except EmptyPage:
        ponderaciones = paginator.page(paginator.num_pages)
    
    context = {'ponderaciones': ponderaciones,}
      
    return render(request, 'rank/myranks.html', context)