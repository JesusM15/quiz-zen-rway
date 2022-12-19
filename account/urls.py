from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('iniciar-sesion/', auth_views.LoginView.as_view(), name='login'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrarse/', views.register, name='register'),
    #cambiar contrasena
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    #resetear contrasena
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('perfiles/ver-perfil-de/<username>/', views.adminPerfil, name='ver_perfil'),
    path('acerca-de/', views.acercade, name='acerca_de'),
    path('ranks/<username>/', views.myranks, name='my_ranks'),
    
]