from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur, OffreDemande, Match

# ============================================================
# PAGE D'ACCUEIL
# ============================================================
def accueil(request):
    return render(request, 'core/accueil.html')

# ============================================================
# INSCRIPTION
# ============================================================
def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        filiere = request.POST.get('filiere')
        niveau = request.POST.get('niveau')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('inscription')

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('inscription')

        utilisateur = Utilisateur.objects.create_user(
            username=username,
            email=email,
            password=password1,
            telephone=telephone,
            filiere=filiere,
            niveau=niveau,
        )
        login(request, utilisateur)
        messages.success(request, "Compte créé avec succès !")
        return redirect('accueil')

    return render(request, 'core/inscription.html', {
        'filieres': Utilisateur.FILIERES
    })

# ============================================================
# CONNEXION
# ============================================================
def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        utilisateur = authenticate(request, username=username, password=password)
        if utilisateur is not None:
            login(request, utilisateur)
            messages.success(request, "Connexion réussie !")
            return redirect('accueil')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('connexion')

    return render(request, 'core/connexion.html')

# ============================================================
# DÉCONNEXION
# ============================================================
@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('connexion')

# ============================================================
# PROFIL
# ============================================================
@login_required
def profil(request):
    return render(request, 'core/profil.html', {
        'utilisateur': request.user
    })