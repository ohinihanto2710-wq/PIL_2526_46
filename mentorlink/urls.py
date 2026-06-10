from django.contrib import admin
from django.urls import path, include
from core import views  # Importe les fonctions de ton application core

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🚨 Routes d'affichage des pages HTML (Sémantiques)
    path('', views.page_connexion, name='page_connexion'),        # Lien : https://onrender.com
    path('register/', views.page_inscription, name='page_inscription'), # Lien : https://onrender.com/register/
    
    # Routes d'API pour les scripts de app.js
    path('api/', include('core.urls')),
]
