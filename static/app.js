// ==============================================================================
// ⚙️ CONFIGURATION GLOBALE DE L'API REST
// ==============================================================================
const API_URL = "https://onrender.com";

// Fonction utilitaire pour récupérer les en-têtes avec le token de sécurité
function getHeaders() {
    const token = localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
    };
}

// ==============================================================================
// 🚀 FONCTION D'INSCRIPTION (Page register.html)
// ==============================================================================
async function inscription(event) {
    if (event) event.preventDefault(); // Empêche le rechargement de la page
    
    const nom = document.getElementById("nom")?.value;
    const email = document.getElementById("email")?.value;
    const password = document.getElementById("password")?.value;
    const role = document.getElementById("role")?.value; 

    if (!nom || !email || !password || !role) {
        alert("Veuillez remplir tous les champs du formulaire.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/auth/register/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nom, email, password, role })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Inscription réussie ! Connectez-vous.");
            window.location.href = "/"; // Redirige vers la page de connexion
        } else {
            alert("Erreur d'inscription : " + (data.error || "Vérifiez vos informations"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Impossible de contacter le serveur backend.");
    }
}

// ==============================================================================
// 🔐 FONCTION DE CONNEXION (Page login.html)
// ==============================================================================
async function connexion(event) {
    if (event) event.preventDefault();
    
    const email = document.getElementById("email")?.value;
    const password = document.getElementById("password")?.value;

    if (!email || !password) {
        alert("Veuillez remplir vos identifiants.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("token", data.access || data.token);
            alert("Connexion réussie ! Bienvenue.");
            window.location.href = "/profil.html"; // Ajuste vers ta page d'accueil après connexion
        } else {
            alert("Erreur de connexion : " + (data.error || "Identifiants incorrects"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Erreur de connexion au serveur.");
    }
}

// ==============================================================================
// 👤 CHARGEMENT DYNAMIQUE DU PROFIL (Page profil.html)
// ==============================================================================
async function chargerProfil() {
    const profName = document.getElementById("prof-name");
    if (!profName) return; // Si on n'est pas sur la page profil, on s'arrête

    try {
        const response = await fetch(`${API_URL}/api/profil/`, {
            method: "GET",
            headers: getHeaders()
        });
        const user = await response.json();

        if (response.ok) {
            if (document.getElementById("prof-name")) document.getElementById("prof-name").innerText = user.nom;
            if (document.getElementById("edit-nom")) document.getElementById("edit-nom").value = user.nom;
            if (document.getElementById("edit-email")) document.getElementById("edit-email").value = user.email;
            
            const zoneSub = document.getElementById("prof-filiere-niveau");
            if (zoneSub && user.role) {
                if (user.role === "les_deux") zoneSub.innerText = "Mentor & Mentoré";
                else if (user.role === "mentor") zoneSub.innerText = "Mentor (Guide)";
                else zoneSub.innerText = "Mentoré (Élève)";
            }
        }
    } catch (error) {
        console.error("Erreur chargement profil :", error);
    }
}

// Déconnexion
function handleLogout() {
    localStorage.removeItem("token");
    alert("Vous avez été déconnecté.");
    window.location.href = "/";
}

// Écouteur automatique au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    chargerProfil();
});
