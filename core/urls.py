from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    
    # Utilisateurs
    path('utilisateurs/', views.liste_utilisateurs, name='utilisateurs'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    
    # Matchs
    path('matches/', views.list_matches, name='list_matches'),
    path('matches/creer/', views.creer_match, name='creer_match'),
    path('matches/<int:match_id>/repondre/', views.repondre_match, name='repondre_match'),
    
    # Disponibilités 
    path('disponibilites/ajouter/', views.ajouter_disponibilite, name='ajouter_disponibilite'),
    path('disponibilites/mentor/<int:mentor_id>/', views.list_disponibilites, name='list_disponibilites'),
    path('disponibilites/mentore/<int:mentore_id>/', views.gerer_disponibilites_mentore, name='disponibilites_mentore'),
    
    # Sessions
    path('sessions/planifier/', views.planifier_session, name='planifier_session'),
    path('sessions/<int:match_id>/', views.list_sessions, name='list_sessions'),
    
    # Messages
    path('messages/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('messages/<int:match_id>/', views.list_messages, name='list_messages'),
    
    # Profil
    path('utilisateurs/<int:utilisateur_id>/', views.profil_utilisateur, name='profil_utilisateur'),
    path('utilisateurs/<int:utilisateur_id>/modifier/', views.modifier_profil, name='modifier_profil'),
    path('utilisateurs/<int:utilisateur_id>/photo/', views.upload_photo, name='upload_photo'),
    path('utilisateurs/<int:utilisateur_id>/upload_page/', views.upload_photo_page, name='upload_photo_page'),
    
    # Mot de passe
    path('reinitialiser-mot-de-passe/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),
    
    # Matching (mentore_id)
    path('matching/<int:mentore_id>/', views.matching, name='matching'),
    
    # Conversations
    path('conversations/<int:utilisateur_id>/', views.list_conversations, name='list_conversations'),
    
    # Offres
    path('offres/', views.list_offres, name='list_offres'),
    path('offres/publier/', views.publier_offre, name='publier_offre'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)