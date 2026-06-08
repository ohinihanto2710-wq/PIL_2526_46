-- Suppression des anciennes tables manuelles si elles existent
DROP TABLE IF EXISTS sessions, messages, matchs, disponibilites, user_competences, competences, utilisateurs CASCADE;

-- Table utilisateurs
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    matricule VARCHAR(10) NOT NULL UNIQUE,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    telephone VARCHAR(20) UNIQUE,
    email_ifri VARCHAR(100) UNIQUE,
    photo_profil VARCHAR(255),
    promo VARCHAR(10) NOT NULL,
    filiere VARCHAR(50) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('mentor', 'mentore', 'les_deux')),
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    bio TEXT,
    points_forts TEXT,
    points_faibles TEXT,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table compétences
CREATE TABLE competences (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

-- Table liaison user <-> compétences
CREATE TABLE user_competences (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    competence_id INT NOT NULL,
    niveau INT CHECK (niveau BETWEEN 1 AND 5),
    FOREIGN KEY (user_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (competence_id) REFERENCES competences(id) ON DELETE CASCADE,
    UNIQUE(user_id, competence_id)
);

-- Table matchs
CREATE TABLE matchs (
    id SERIAL PRIMARY KEY,
    mentor_id INT NOT NULL,
    mentore_id INT NOT NULL,
    statut VARCHAR(15) DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'accepte', 'termine', 'annule')),
    date_match TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    objectif TEXT,
    FOREIGN KEY (mentor_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (mentore_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    UNIQUE(mentor_id, mentore_id)
);

-- Table messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matchs(id) ON DELETE CASCADE,
    FOREIGN KEY (expediteur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table disponibilités
CREATE TABLE disponibilites (
    id SERIAL PRIMARY KEY,
    mentor_id INT NOT NULL,
    jour VARCHAR(10) NOT NULL CHECK (jour IN ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche')),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    FOREIGN KEY (mentor_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    UNIQUE(mentor_id, jour, heure_debut)
);

-- Table sessions
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL,
    date_session TIMESTAMP NOT NULL,
    duree INT NOT NULL,
    statut VARCHAR(15) DEFAULT 'planifiee' CHECK (statut IN ('planifiee', 'faite', 'annulee')),
    notes TEXT,
    FOREIGN KEY (match_id) REFERENCES matchs(id) ON DELETE CASCADE
);

-- Table offres et demandes de mentorat
CREATE TABLE offres (
    id SERIAL PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    type_offre VARCHAR(10) NOT NULL CHECK (type_offre IN ('offre', 'demande')),
    competences TEXT NOT NULL,
    disponibilites TEXT NOT NULL,
    format VARCHAR(20) DEFAULT 'les_deux' CHECK (format IN ('presentiel', 'enligne', 'les_deux')),
    description TEXT,
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);
