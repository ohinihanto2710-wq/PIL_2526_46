from django.contrib import admin

# Register your models here.
from .models import Utilisateur, Competence, UserCompetence, Match, Message, Disponibilite, Session

admin.site.register(Utilisateur)
admin.site.register(Competence)
admin.site.register(UserCompetence)
admin.site.register(Match)
admin.site.register(Message)
admin.site.register(Disponibilite)
admin.site.register(Session)