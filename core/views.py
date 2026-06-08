from .models import Utilisateur, OffreDemande, Match, Conversation, Message

# Create your views here.
# ============================================================
# OFFRES ET DEMANDES
# ============================================================
@login_required
def poster_demande(request):
    if request.method == 'POST':
        matiere = request.POST.get('matiere')
        disponibilites = request.POST.get('disponibilites')
        format_session = request.POST.get('format_session')
        type_annonce = request.POST.get('type_annonce')

        OffreDemande.objects.create(
            utilisateur=request.user,
            type_annonce=type_annonce,
            matiere=matiere,
            disponibilites=disponibilites,
            format_session=format_session,
        )
        messages.success(request, "Votre annonce a été publiée avec succès !")
        return redirect('accueil')

    return render(request, 'core/poster_demande.html', {
        'formats': OffreDemande.FORMAT_CHOICES,
        'types': OffreDemande.TYPE_CHOICES,
    })

@login_required
def liste_mentors(request):
    mentors = OffreDemande.objects.filter(
        type_annonce='offre'
    ).select_related('utilisateur')
    return render(request, 'core/liste_mentors.html', {
        'mentors': mentors
    })

@login_required
def liste_mentores(request):
    mentores = OffreDemande.objects.filter(
        type_annonce='demande'
    ).select_related('utilisateur')
    return render(request, 'core/liste_mentores.html', {
        'mentores': mentores
    })

# ============================================================
# ALGORITHME DE MATCHING
# ============================================================
@login_required
def matching(request):
    utilisateur = request.user
    matchs = []

    # Récupère les annonces de l'utilisateur
    mes_annonces = OffreDemande.objects.filter(utilisateur=utilisateur)

    for annonce in mes_annonces:
        # Cherche les annonces opposées avec la même matière
        if annonce.type_annonce == 'demande':
            annonces_opposees = OffreDemande.objects.filter(
                type_annonce='offre',
                matiere=annonce.matiere
            ).exclude(utilisateur=utilisateur)
        else:
            annonces_opposees = OffreDemande.objects.filter(
                type_annonce='demande',
                matiere=annonce.matiere
            ).exclude(utilisateur=utilisateur)

        for ao in annonces_opposees:
            # Calcul du score
            score = 0.0

            # +50 points si même matière (déjà filtré)
            score += 50.0

            # +30 points si même filière
            if ao.utilisateur.filiere == utilisateur.filiere:
                score += 30.0

            # +20 points si format compatible
            if (annonce.format_session == ao.format_session or
                annonce.format_session == 'les2' or
                ao.format_session == 'les2'):
                score += 20.0

            matchs.append({
                'utilisateur': ao.utilisateur,
                'annonce': ao,
                'score': score,
            })

    # Trie par score décroissant
    matchs = sorted(matchs, key=lambda x: x['score'], reverse=True)

    # Sauvegarde les matchs en base de données
    for m in matchs:
        if utilisateur.username != m['utilisateur'].username:
            Match.objects.get_or_create(
                mentor=m['utilisateur'] if m['annonce'].type_annonce == 'offre' else utilisateur,
                mentore=utilisateur if m['annonce'].type_annonce == 'offre' else m['utilisateur'],
                defaults={'score': m['score']}
            )

    return render(request, 'core/matching.html', {
        'matchs': matchs
    })

# ============================================================
# MESSAGERIE
# ============================================================
@login_required
def liste_conversations(request):
    # Récupère toutes les conversations de l'utilisateur connecté
    conversations = Conversation.objects.filter(
        participants=request.user
    ).order_by('-date_creation')
    return render(request, 'core/conversations.html', {
        'conversations': conversations
    })

@login_required
def detail_conversation(request, conversation_id):
    # Récupère la conversation ou retourne une erreur 404
    try:
        conversation = Conversation.objects.get(
            id=conversation_id,
            participants=request.user
        )
    except Conversation.DoesNotExist:
        messages.error(request, "Conversation introuvable.")
        return redirect('liste_conversations')

    # Récupère tous les messages de la conversation
    tous_messages = Message.objects.filter(
        conversation=conversation
    ).order_by('date_envoi')

    # Marque les messages non lus comme lus
    Message.objects.filter(
        conversation=conversation,
        lu=False
    ).exclude(expediteur=request.user).update(lu=True)

    # Envoi d'un nouveau message
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Message.objects.create(
                conversation=conversation,
                expediteur=request.user,
                contenu=contenu,
            )
            return redirect('detail_conversation', conversation_id=conversation_id)

    return render(request, 'core/detail_conversation.html', {
        'conversation': conversation,
        'tous_messages': tous_messages,
    })

@login_required
def demarrer_conversation(request, utilisateur_id):
    # Récupère l'autre utilisateur
    try:
        autre_utilisateur = Utilisateur.objects.get(id=utilisateur_id)
    except Utilisateur.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('accueil')

    # Vérifie si une conversation existe déjà entre les deux
    conversation_existante = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=autre_utilisateur
    ).first()

    if conversation_existante:
        # Si elle existe déjà, on y redirige directement
        return redirect('detail_conversation', conversation_id=conversation_existante.id)

    # Sinon on crée une nouvelle conversation
    nouvelle_conversation = Conversation.objects.create()
    nouvelle_conversation.participants.add(request.user, autre_utilisateur)
    nouvelle_conversation.save()

    return redirect('detail_conversation', conversation_id=nouvelle_conversation.id)