from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    FILIERES = [
        ('IA', 'Intelligence Artificielle'),
        ('IM', 'Ingénierie Mathématique'),
        ('GL', 'Génie Logiciel'),
        ('SE', 'Systèmes Embarqués & IoT'),
        ('SI', 'Systèmes d\'Information'),
    ]
    telephone = models.CharField(max_length=20, unique=True)
    filiere = models.CharField(max_length=10, choices=FILIERES)
    niveau = models.CharField(max_length=10)
    photo = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True)
    disponibilites = models.TextField(blank=True)

class Competence(models.Model):
    nom = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='competences')
    est_point_fort = models.BooleanField(default=True)

class OffreDemande(models.Model):
    TYPE_CHOICES = [('offre', 'Offre'), ('demande', 'Demande')]
    FORMAT_CHOICES = [('presentiel', 'Présentiel'), ('enligne', 'En ligne'), ('les2', 'Les deux')]
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_annonce = models.CharField(max_length=10, choices=TYPE_CHOICES)
    matiere = models.CharField(max_length=100)
    disponibilites = models.TextField()
    format_session = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)

class Match(models.Model):
    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchs_mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchs_mentore')
    score = models.FloatField(default=0.0)
    date_match = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    participants = models.ManyToManyField(Utilisateur)
    date_creation = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)