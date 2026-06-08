from django.shortcuts import render

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