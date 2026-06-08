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

    # Messagerie
    path('conversations/', views.liste_conversations, name='liste_conversations'),
    path('conversations/<int:conversation_id>/', views.voir_conversation, name='voir_conversation'),
    path('conversations/<int:conversation_id>/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('nouvelle-conversation/<int:utilisateur_id>/', views.nouvelle_conversation, name='nouvelle_conversation'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
]