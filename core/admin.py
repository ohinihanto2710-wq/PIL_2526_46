from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Competence, OffreDemande, Match, Conversation, Message

admin.site.register(Utilisateur, UserAdmin)
admin.site.register(Competence)
admin.site.register(OffreDemande)
admin.site.register(Match)
admin.site.register(Conversation)
admin.site.register(Message)