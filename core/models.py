from django.db import models

# Create your models here.
class Utilisateur(models.Model):
    ROLES = [
        ('mentor', 'Mentor'),
        ('mentore', 'Mentoré'),
        ('les_deux', 'Les deux'),
    ]
    matricule = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email_ifri = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    photo_profil = models.CharField(max_length=255, null=True, blank=True)
    promo = models.CharField(max_length=10)
    filiere = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLES, default='mentore')
    mot_de_passe_hash = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    points_forts = models.TextField(null=True, blank=True)
    points_faibles = models.TextField(null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.nom} {self.prenom}"

class Competence(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def _str_(self):
        return self.nom

class UserCompetence(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    niveau = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'competence')

class Match(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchs_mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchs_mentore')
    statut = models.CharField(max_length=15, choices=STATUTS, default='en_attente')
    date_match = models.DateTimeField(auto_now_add=True)
    objectif = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('mentor', 'mentore')

class Message(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

class Disponibilite(models.Model):  
    JOURS = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ]
    
    mentor = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='disponibilites')
    jour = models.CharField(max_length=10, choices=JOURS)  
    heure_debut = models.TimeField()  
    heure_fin = models.TimeField()    
    
    class Meta:
        unique_together = ('mentor', 'jour', 'heure_debut')
    
    def _str_(self):
        return f"{self.mentor.nom} - {self.jour} ({self.heure_debut} à {self.heure_fin})"
class DisponibiliteMentore(models.Model):
    JOURS = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ]
    
    mentore = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='disponibilites_mentore')
    jour = models.CharField(max_length=10, choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    
    class Meta:
        db_table = 'disponibilites_mentores'
        unique_together = ('mentore', 'jour', 'heure_debut')
    
    def _str_(self):
        return f"{self.mentore.nom} {self.mentore.prenom}- {self.jour} ({self.heure_debut} à {self.heure_fin})"

class Session(models.Model):
    STATUTS = [
        ('planifiee', 'Planifiée'),
        ('faite', 'Faite'),
        ('annulee', 'Annulée'),
    ]
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    date_session = models.DateTimeField()
    duree = models.IntegerField()
    statut = models.CharField(max_length=15, choices=STATUTS, default='planifiee')
    notes = models.TextField(null=True, blank=True)
class Offre(models.Model):
    TYPES = [
        ('offre', 'Offre de mentorat'),
        ('demande', 'Demande de mentorat'),
    ]
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_offre = models.CharField(max_length=10, choices=TYPES)
    competences = models.TextField()
    disponibilites = models.TextField()
    format = models.CharField(max_length=20, default='les_deux',
        choices=[('presentiel', 'Présentiel'), ('enligne', 'En ligne'), ('les_deux', 'Les deux')])
    description = models.TextField(null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.type_offre} - {self.utilisateur.nom}"