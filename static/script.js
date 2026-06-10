// ==============================================================================
// 🚀 CONFIGURATION DIRECTE ET COMPLÈTE DE L'INSCRIPTION
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
        // 🚨 L'ADRESSE OFFICIELLE EST ÉCRITE ICI DIRECTEMENT EN DUR !
        const response = await fetch("https://onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nom, email, password, role })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Inscription réussie ! Vous allez être redirigé vers la page de connexion.");
            window.location.href = "/"; // Redirige vers la racine (login)
        } else {
            alert("Erreur d'inscription : " + (data.error || "Vérifiez vos informations"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Impossible de contacter le serveur backend.");
    }
}

// ==============================================================================
// 🔐 CONFIGURATION DIRECTE ET COMPLÈTE DE LA CONNEXION
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
        // 🚨 L'ADRESSE OFFICIELLE POUR LA CONNEXION !
        const response = await fetch("https://onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("token", data.access || data.token);
            alert("Connexion réussie ! Bienvenue.");
            window.location.href = "/profil.html"; // Redirige vers le profil
        } else {
            alert("Erreur de connexion : " + (data.error || "Identifiants incorrects"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Erreur de connexion au serveur.");
    }
}
