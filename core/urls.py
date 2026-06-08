from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('poster-demande/', views.poster_demande, name='poster_demande'),
    path('mentors/', views.liste_mentors, name='liste_mentors'),
    path('mentores/', views.liste_mentores, name='liste_mentores'),
    path('matching/', views.matching, name='matching'),
]