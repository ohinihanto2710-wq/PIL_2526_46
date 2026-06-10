from django.contrib import admin
from django.urls import path, include
from core import views  # 🚨 Ligne obligatoire pour éviter l'erreur "views is not defined" !

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.page_accueil_redirection, name='accueil_login'),  # Route vers la page de connexion
    path('api/', include('core.urls')),  # Vos routes d'API existantes
]
