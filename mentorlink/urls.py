from django.contrib import admin
from django.urls import path, include
from core import views  # Ligne indispensable

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.page_accueil_redirection, name='accueil_login'),
    path('api/', include('core.urls')),
]
