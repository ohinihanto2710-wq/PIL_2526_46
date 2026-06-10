from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register),
    path('auth/login/', views.login),
    path('profil/', views.profil),
    path('utilisateurs/', views.utilisateurs),
    path('offres/', views.offres),
    path('conversations/creer/', views.creer_conversation),
    path('conversations/<int:conv_id>/messages/', views.messages),
]