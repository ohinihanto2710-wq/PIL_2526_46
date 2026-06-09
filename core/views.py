from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods    
from django.contrib.auth.decorators import permission_required  
from django.db.models import Q    
from django.contrib.auth.hashers import make_password, check_password 
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os                
import json
from .models import Utilisateur, Competence, Match, Session, Disponibilite, DisponibiliteMentore  
def index(request):
    return JsonResponse({'message': 'BIENVENUE SUR IFRI_MENTORLINK'})

def liste_competences(request):
    competences = Competence.objects.all().values('id', 'nom')
    return JsonResponse(list(competences), safe=False)

def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all().values('id', 'nom', 'matricule', 'role', 'filiere')
    return JsonResponse(list(utilisateurs), safe=False)

@csrf_exempt
def inscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if Utilisateur.objects.filter(matricule=data['matricule']).exists():
            return JsonResponse({'erreur': 'Matricule déjà utilisé'}, status=400)
        if data.get('telephone') and Utilisateur.objects.filter(telephone=data['telephone']).exists():
            return JsonResponse({'erreur': 'Téléphone déjà utilisé'}, status=400)
        if data.get('email_ifri') and Utilisateur.objects.filter(email_ifri=data['email_ifri']).exists():
            return JsonResponse({'erreur': 'Email déjà utilisé'}, status=400)
        utilisateur = Utilisateur.objects.create(
            matricule=data['matricule'],
            nom=data['nom'],
            prenom=data['prenom'],
            telephone=data.get('telephone'),
            email_ifri=data.get('email_ifri'),
            promo=data['promo'],
            filiere=data['filiere'],
            role=data['role'],
            mot_de_passe_hash=make_password(data['mot_de_passe_hash']),
            bio=data.get('bio'),
            points_forts=data.get('points_forts'),
            points_faibles=data.get('points_faibles')
        )
        return JsonResponse({'message': 'Inscription réussie', 'id': utilisateur.id}, status=201)
    return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def connexion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identifiant = data.get('identifiant')
            mot_de_passe = data.get('mot_de_passe')
            
            # Recherche par matricule, email ou téléphone
            utilisateur = Utilisateur.objects.filter(
                Q(matricule=identifiant) |
                Q(email_ifri=identifiant) |
                Q(telephone=identifiant)
            ).first()
            
            if utilisateur and check_password(mot_de_passe, utilisateur.mot_de_passe_hash):
                # Créer la session
                request.session['user_id'] = utilisateur.id
                request.session['user_nom'] = f"{utilisateur.prenom} {utilisateur.nom}"
                request.session['user_role'] = utilisateur.role
                
                return JsonResponse({
                    'success': True,
                    'message': 'Connexion réussie',
                    'user_id': utilisateur.id,
                    'nom': utilisateur.nom,
                    'prenom': utilisateur.prenom,
                    'role': utilisateur.role
                }, status=200)
            else:
                return JsonResponse({'erreur': 'Identifiants invalides'}, status=401)
                
        except Exception as e:
            return JsonResponse({'erreur': str(e)}, status=400)
    
    return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
@csrf_exempt
def creer_match(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mentor = Utilisateur.objects.get(id=data['mentor_id'])
        mentore = Utilisateur.objects.get(id=data['mentore_id'])
        if Match.objects.filter(mentor=mentor, mentore=mentore).exists():
            return JsonResponse({'erreur': 'Match déjà existant'}, status=400)
        match = Match.objects.create(
            mentor=mentor,
            mentore=mentore,
            objectif=data.get('objectif')
        )
        return JsonResponse({'message': 'Demande de mentorat envoyé!', 'id': match.id}, status=201)
    return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def repondre_match(request, match_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            match = Match.objects.get(id=match_id)
            match.statut = data['statut']
            match.save()
            if match.statut == 'accepte':
             msg = 'Demande de mentorat acceptée !'
            elif match.statut == 'annule':
             msg = 'Demande de mentorat refusée'
            elif match.statut == 'termine':
             msg = 'Session de mentorat terminée'
            else:
             msg = 'Statut mis à jour'
            return JsonResponse({'message': msg, 'statut': match.statut})
        except Match.DoesNotExist:
         return JsonResponse({'erreur': 'Demande de mentorat introuvable'}, status=404)
    return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)

def list_matches(request):
    matchs = Match.objects.all().values(
        'id', 'mentor_id', 'mentore_id', 'statut', 'objectif', 'date_match'
    )
    return JsonResponse(list(matchs), safe=False)
@csrf_exempt
def ajouter_disponibilite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            mentor = Utilisateur.objects.get(id=data['mentor_id'])
            dispo = Disponibilite.objects.create(
                mentor=mentor,
                jour=data['jour'],
                heure_debut=data['heure_debut'],
                heure_fin=data['heure_fin']
            )
            return JsonResponse({'message': 'Disponibilité ajoutée', 'id': dispo.id}, status=201)
        except Utilisateur.DoesNotExist:
            return JsonResponse({'erreur': 'Mentor introuvable'}, status=404)
    return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)

def list_disponibilites(request, mentor_id):
    dispos = Disponibilite.objects.filter(mentor_id=mentor_id).values(
        'id', 'jour', 'heure_debut', 'heure_fin'
    )
    return JsonResponse(list(dispos), safe=False)


@csrf_exempt
def planifier_session(request):
    if request.method != 'POST':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    
    try:
        data = json.loads(request.body)
        match = Match.objects.get(id=data['match_id'])
        
        session = Session.objects.create(
            match=match,
            date_session=data['date_session'],
            duree=data['duree'],
            statut='planifiee',
            notes=data.get('notes', '')
        )
        
        return JsonResponse({'message': 'Session planifiée', 'id': session.id}, status=201)
    
    except Match.DoesNotExist:
        return JsonResponse({'erreur': 'Match introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=400)
def list_sessions(request, match_id):
    """Liste toutes les sessions d'un match"""
    try:
        match = Match.objects.get(id=match_id)
        sessions = Session.objects.filter(match=match).order_by('date_session')
        
        data = []
        for s in sessions:
            data.append({
              'id': s.id,
              'match_id': s.match.id,
              'date_session': s.date_session.strftime('%Y-%m-%d %H:%M'),
              'duree': s.duree,
              'statut': s.statut,
              'notes': s.notes
        } )
        
        return JsonResponse(data, safe=False, status=200)
    
    except Match.DoesNotExist:
        return JsonResponse({'erreur': 'Match introuvable'}, status=404)
def matching(request, mentore_id):
    try:
        mentore = Utilisateur.objects.get(id=mentore_id)
        points_faibles = [p.strip().lower() for p in (mentore.points_faibles or '').split(',') if p.strip()]
        filiere_mentore = mentore.filiere

        mentors = Utilisateur.objects.filter(
            role__in=['mentor', 'les_deux']
        ).exclude(id=mentore_id)

        resultats = []

        for mentor in mentors:
            score = 0
            points_forts = [p.strip().lower() for p in (mentor.points_forts or '').split(',') if p.strip()]

            # 1. Compatibilité des compétences
            competences_communes = [p for p in points_faibles if p in points_forts]
            score += len(competences_communes) * 30

            # 2. Proximité des filières
            if mentor.filiere == filiere_mentore:
                score += 20

            # 3. Compatibilité des horaires
            # Table pour mentors : disponibilites
            dispos_mentor = Disponibilite.objects.filter(mentor_id=mentor.id)
            # Table pour mentorés : disponibilites_mentores
            dispos_mentore = DisponibiliteMentore.objects.filter(mentore_id=mentore.id)

            horaires_compatibles = 0
            horaires_detail = []

            for dispo_m in dispos_mentor:
                for dispo_mt in dispos_mentore:
                    if (dispo_m.jour == dispo_mt.jour and
                        dispo_m.heure_debut < dispo_mt.heure_fin and
                        dispo_m.heure_fin > dispo_mt.heure_debut):

                        horaires_compatibles += 1
                        debut_compatible = max(dispo_m.heure_debut, dispo_mt.heure_debut)
                        fin_compatible = min(dispo_m.heure_fin, dispo_mt.heure_fin)

                        horaires_detail.append({
                            'jour': dispo_m.jour,
                            'debut': debut_compatible.strftime('%H:%M'),
                            'fin': fin_compatible.strftime('%H:%M')
                        })

            if horaires_compatibles > 0:
                score += 10
                score += min(horaires_compatibles, 5)
            else:
                if dispos_mentor.exists():
                    score += 3

            resultats.append({
                'mentor_id': mentor.id,
                'nom': mentor.nom,
                'prenom': mentor.prenom,
                'filiere': mentor.filiere,
                'points_forts': mentor.points_forts,
                'competences_communes': competences_communes,
                'score': score,
                'horaires_compatibles': horaires_compatibles,
                'creneaux': horaires_detail
            })

        resultats.sort(key=lambda x: x['score'], reverse=True)
        return JsonResponse(resultats, safe=False, status=200)

    except Utilisateur.DoesNotExist:
        return JsonResponse({'erreur': 'Mentoré introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=500)
#liste des conversations
def list_conversations(request, utilisateur_id):
    """Liste toutes les conversations d'un utilisateur"""
    try:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        
        # Récupérer tous les matchs de l'utilisateur (acceptés ou en cours)
        matches = Match.objects.filter(
            Q(mentor_id=utilisateur_id) | Q(mentore_id=utilisateur_id)
        ).exclude(statut='annule')
        
        conversations = []
        
        for match in matches:
            # Identifier l'interlocuteur
            if match.mentor_id == utilisateur_id:
                interlocuteur = match.mentore
                role = "mentor"
            else:
                interlocuteur = match.mentor
                role = "mentore"
            
            # Récupérer le dernier message
            dernier_message = Message.objects.filter(match=match).order_by('-date_envoi').first()
            
            # Compter les messages non lus (optionnel)
            # non_lus = Message.objects.filter(match=match, expediteur=interlocuteur, lu=False).count()
            
            conversations.append({
                'match_id': match.id,
                'interlocuteur': {
                    'id': interlocuteur.id,
                    'nom': interlocuteur.nom,
                    'prenom': interlocuteur.prenom,
                    'photo_profil': interlocuteur.photo_profil,
                    'filiere': interlocuteur.filiere
                },
                'role': role,
                'statut_match': match.statut,
                'dernier_message': {
                    'contenu': dernier_message.contenu if dernier_message else None,
                    'date_envoi': dernier_message.date_envoi.strftime('%Y-%m-%d %H:%M') if dernier_message else None,
                    'expediteur_id': dernier_message.expediteur_id if dernier_message else None
                } if dernier_message else None,
                'date_match': match.date_match.strftime('%Y-%m-%d %H:%M')
            })
        
        # Trier par date du dernier message (plus récent en premier)
        conversations.sort(key=lambda x: x['dernier_message']['date_envoi'] if x['dernier_message'] else '', reverse=True)
        
        return JsonResponse(conversations, safe=False, status=200)
    
    except Utilisateur.DoesNotExist:
        return JsonResponse({'erreur': 'Utilisateur introuvable'}, status=404)
# photo de profil
@csrf_exempt
def upload_photo(request, utilisateur_id):
    """Uploader une photo de profil"""
    if request.method != 'POST':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    
    try:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        
        if 'photo' not in request.FILES:
            return JsonResponse({'erreur': 'Aucune photo envoyée'}, status=400)
        
        photo = request.FILES['photo']
        
        # Vérifier le type de fichier
        if not photo.content_type.startswith('image/'):
            return JsonResponse({'erreur': 'Le fichier doit être une image'}, status=400)
        
        # Sauvegarder
        utilisateur.photo_profil.save(photo.name, photo)
        utilisateur.save()
        
        return JsonResponse({
            'message': 'Photo uploadée avec succès',
            'photo_profil': utilisateur.photo_profil.url if utilisateur.photo_profil else None
        }, status=200)
    
    except Utilisateur.DoesNotExist:
        return JsonResponse({'erreur': 'Utilisateur introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=400)
# informations sue le profil d'un utilisateur
def profil_utilisateur(request, utilisateur_id):
    try:
        # Test 1 : Vérifier que la fonction est appelée
        print(f"=== Vue appelée avec ID: {utilisateur_id} ===")
        
        # Test 2 : Vérifier le modèle
        from .models import Utilisateur
        print("Modèle Utilisateur importé avec succès")
        
        # Test 3 : Récupérer l'utilisateur
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        print(f"Utilisateur trouvé: {utilisateur.nom}")
        
        # Test 4 : Retourner une réponse simple
        return JsonResponse({
            'success': True,
            'id': utilisateur.id,
            'nom': utilisateur.nom,
            'prenom': utilisateur.prenom
        }, status=200)
    
    except Utilisateur.DoesNotExist:
        print(f"ERREUR: Utilisateur {utilisateur_id} non trouvé")
        return JsonResponse({'erreur': f'Utilisateur {utilisateur_id} introuvable'}, status=404)
    
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'erreur': str(e)}, status=500)
#  vues des demandes d'offre et de mentorat sur la page
@csrf_exempt
def publier_offre(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            from .models import Offre 
            utilisateur = Utilisateur.objects.get(id=data['utilisateur_id'])
            offre = Offre.objects.create(
                utilisateur=utilisateur,
                type_offre=data['type_offre'],
                competences=data['competences'],
                disponibilites=data['disponibilites'],
                format=data.get('format', 'les_deux'),
                description=data.get('description')
            )
            return JsonResponse({'message': 'Offre publiée avec succès', 'id': offre.id}, status=201)
        except Utilisateur.DoesNotExist:
            return JsonResponse({'erreur': 'Utilisateur introuvable'}, status=404)
    return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)

def list_offres(request):
    type_offre = request.GET.get('type')
    competence = request.GET.get('competence')
    
    offres = Offre.objects.filter(active=True)
    
    if type_offre:
        offres = offres.filter(type_offre=type_offre)
    if competence:
        offres = offres.filter(competences__icontains=competence)
    
    resultats = []
    for offre in offres:
        resultats.append({
            'id': offre.id,
            'utilisateur_id': offre.utilisateur.id,
            'nom': offre.utilisateur.nom,
            'prenom': offre.utilisateur.prenom,
            'filiere': offre.utilisateur.filiere,
            'type_offre': offre.type_offre,
            'competences': offre.competences,
            'disponibilites': offre.disponibilites,
            'format': offre.format,
            'description': offre.description,
            'date_publication': str(offre.date_publication)
        })
    
    return JsonResponse(resultats, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def gerer_disponibilites_mentore(request, mentore_id):
    """Gère les disponibilités d'un mentoré (GET, POST, DELETE)"""
    
    if request.method == "GET":
        # Récupérer toutes les disponibilités du mentoré
        dispos = DisponibiliteMentore.objects.filter(mentore_id=mentore_id)
        data = [{
            'id': d.id,
            'jour': d.jour,
            'heure_debut': d.heure_debut.strftime('%H:%M'),
            'heure_fin': d.heure_fin.strftime('%H:%M')
        } for d in dispos]
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        # Ajouter une nouvelle disponibilité
        try:
            data = json.loads(request.body)
            
            # Vérifier que le mentoré existe
            mentore = Utilisateur.objects.get(id=mentore_id)
            
            # Créer la disponibilité
            disponibilite = DisponibiliteMentore.objects.create(
                mentore=mentore,
                jour=data['jour'],
                heure_debut=data['heure_debut'],
                heure_fin=data['heure_fin']
            )
            
            return JsonResponse({
                'id': disponibilite.id,
                'message': 'Disponibilité ajoutée avec succès'
            }, status=201)
        except Utilisateur.DoesNotExist:
            return JsonResponse({'erreur': 'Mentoré introuvable'}, status=404)
        except Exception as e:
            return JsonResponse({'erreur': str(e)}, status=400)
    
    elif request.method == "DELETE":
        # Supprimer une disponibilité (passer l'id en paramètre ?id=xxx)
        try:
            dispo_id = request.GET.get('id')
            if not dispo_id:
                return JsonResponse({'erreur': 'Paramètre id requis'}, status=400)
            
            disponibilite = DisponibiliteMentore.objects.get(id=dispo_id, mentore_id=mentore_id)
            disponibilite.delete()
            
            return JsonResponse({'message': 'Disponibilité supprimée avec succès'}, status=200)
        except DisponibiliteMentore.DoesNotExist:
            return JsonResponse({'erreur': 'Disponibilité introuvable'}, status=404)
        except Exception as e:
            return JsonResponse({'erreur': str(e)}, status=400)
# ========== MESSAGES ==========
@csrf_exempt
def envoyer_message(request):
    if request.method != 'POST':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    try:
        data = json.loads(request.body)
        message = Message.objects.create(
            match_id=data['match_id'],
            expediteur_id=data['expediteur_id'],
            contenu=data['contenu']
        )
        return JsonResponse({'id': message.id, 'message': 'Message envoyé'}, status=201)
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=400)
def list_messages(request, match_id):
    """Liste tous les messages d'un match spécifique"""
    try:
        match = Match.objects.get(id=match_id)
        from .models import Message
        messages = Message.objects.filter(match=match).order_by('date_envoi')
        
        data = [{
            'id': m.id,
            'expediteur_id': m.expediteur_id,
            'expediteur_nom': f"{m.expediteur.prenom} {m.expediteur.nom}",
            'contenu': m.contenu,
            'date_envoi': m.date_envoi.strftime('%Y-%m-%d %H:%M:%S')
        } for m in messages]
        
        return JsonResponse(data, safe=False, status=200)
    
    except Match.DoesNotExist:
        return JsonResponse({'erreur': 'Match introuvable'}, status=404)
@csrf_exempt
def modifier_profil(request, utilisateur_id):
    """Modifier le profil d'un utilisateur"""
    
    if request.method != 'POST' and request.method != 'PUT':
        return JsonResponse({'erreur': 'Méthode non autorisée. Utilisez POST ou PUT'}, status=405)
    
    try:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        data = json.loads(request.body)
        
        # Champs modifiables
        champs_autorises = [
            'nom', 'prenom', 'telephone', 'email_ifri', 'bio',
            'points_forts', 'points_faibles', 'filiere', 'promo', 'role'
        ]
        
        for champ in champs_autorises:
            if champ in data:
                setattr(utilisateur, champ, data[champ])
        
        utilisateur.save()
        
        # Retourner le profil mis à jour
        return JsonResponse({
            'message': 'Profil mis à jour avec succès',
            'utilisateur': {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'telephone': utilisateur.telephone,
                'email_ifri': utilisateur.email_ifri,
                'bio': utilisateur.bio,
                'points_forts': utilisateur.points_forts,
                'points_faibles': utilisateur.points_faibles,
                'filiere': utilisateur.filiere,
                'promo': utilisateur.promo,
                'role': utilisateur.role,
                'photo_profil': utilisateur.photo_profil
            }
        }, status=200)
    
    except Utilisateur.DoesNotExist:
        return JsonResponse({'erreur': 'Utilisateur introuvable'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'erreur': 'Format JSON invalide'}, status=400)
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=400)
@csrf_exempt
def reinitialiser_mot_de_passe(request):
    """Version simplifiée : changement direct avec identifiant + nouveau mot de passe"""
    
    if request.method != 'POST':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        identifiant = data.get('identifiant')
        nouveau_mot_de_passe = data.get('nouveau_mot_de_passe')
        confirmer_mot_de_passe = data.get('confirmer_mot_de_passe')
        
        if not identifiant or not nouveau_mot_de_passe:
            return JsonResponse({'erreur': 'Identifiant et nouveau mot de passe requis'}, status=400)
        
        if nouveau_mot_de_passe != confirmer_mot_de_passe:
            return JsonResponse({'erreur': 'Les mots de passe ne correspondent pas'}, status=400)
        
        # Chercher l'utilisateur
        utilisateur = Utilisateur.objects.filter(
            Q(email_ifri=identifiant) | 
            Q(telephone=identifiant) | 
            Q(matricule=identifiant)
        ).first()
        
        if not utilisateur:
            return JsonResponse({'erreur': 'Utilisateur introuvable'}, status=404)
        
        # Mettre à jour le mot de passe
        utilisateur.mot_de_passe_hash = make_password(nouveau_mot_de_passe)
        utilisateur.save()
        
        return JsonResponse({'message': 'Mot de passe réinitialisé avec succès'}, status=200)
    
    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=400)
def upload_photo_page(request, utilisateur_id):
        return render(request,'upload_photo.html',{'utilisateur_id':utilisateur_id})