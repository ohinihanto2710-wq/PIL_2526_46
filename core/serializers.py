from rest_framework import serializers
from .models import Utilisateur, Competence, OffreDemande, Message, Conversation

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'nom', 'est_point_fort']

class UtilisateurSerializer(serializers.ModelSerializer):
    competences = CompetenceSerializer(many=True, read_only=True)
    class Meta:
        model = Utilisateur
        fields = ['id', 'first_name', 'last_name', 'email', 'telephone',
                  'filiere', 'niveau', 'bio', 'disponibilites', 'photo', 'competences']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'telephone',
                  'filiere', 'niveau', 'password']
    def create(self, data):
        user = Utilisateur.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            telephone=data['telephone'],
            filiere=data['filiere'],
            niveau=data['niveau'],
        )
        return user

class OffreDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffreDemande
        fields = ['id', 'type_annonce', 'matiere', 'disponibilites',
                  'format_session', 'date_creation']

class MessageSerializer(serializers.ModelSerializer):
    expediteur_nom = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['id', 'contenu', 'date_envoi', 'lu', 'expediteur_nom', 'expediteur']
    def get_expediteur_nom(self, obj):
        return obj.expediteur.first_name + ' ' + obj.expediteur.last_name

class ConversationSerializer(serializers.ModelSerializer):
    participants = UtilisateurSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'date_creation']