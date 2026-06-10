/* =============================================
   IFRI_MentorLink — app.js
   ============================================= */

// ── NAVBAR MOBILE ──
const menuToggle = document.getElementById('menuToggle');
const navbar = document.querySelector('.navbar');
if (menuToggle) {
  menuToggle.addEventListener('click', () => navbar.classList.toggle('open'));
}

// ── TOGGLE PASSWORD VISIBILITY ──
function togglePwd(id, btn) {
  const input = document.getElementById(id);
  if (input.type === 'password') {
    input.type = 'text';
    if (btn) btn.innerHTML = '<i class="fa fa-eye-slash"></i>';
  } else {
    input.type = 'password';
    if (btn) btn.innerHTML = '<i class="fa fa-eye"></i>';
  }
}

// ── SHOW FORM MESSAGE ──
function showMsg(id, text, type = 'error') {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = text;
  el.className = 'form-msg ' + type;
  el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 4000);
}

// ── MODAL ──
function closeModal(id) { document.getElementById(id).style.display = 'none'; }
window.addEventListener('click', (e) => {
  document.querySelectorAll('.modal-overlay').forEach(m => {
    if (e.target === m) m.style.display = 'none';
  });
});

// ── LOGIN ──
function handleLogin() {
  const id = document.getElementById('loginId')?.value.trim();
  const pwd = document.getElementById('loginPwd')?.value;
  if (!id || !pwd) { showMsg('loginMsg', 'Veuillez remplir tous les champs.'); return; }
  if (pwd.length < 6) { showMsg('loginMsg', 'Mot de passe trop court (6 caractères min).'); return; }
  showMsg('loginMsg', 'Connexion réussie ! Redirection…', 'success');
  setTimeout(() => { window.location.href = 'profil.html'; }, 1200);
}

// ── REGISTER STEPS ──
function nextStep(n) {
  if (n === 2) {
    const prenom = document.getElementById('reg-prenom')?.value.trim();
    const nom = document.getElementById('reg-nom')?.value.trim();
    const email = document.getElementById('reg-email')?.value.trim();
    const tel = document.getElementById('reg-tel')?.value.trim();
    const filiere = document.getElementById('reg-filiere')?.value;
    const niveau = document.getElementById('reg-niveau')?.value;
    if (!prenom || !nom || !email || !tel || !filiere || !niveau) {
      showMsg('regMsg', 'Veuillez remplir tous les champs obligatoires.'); return;
    }
    if (!email.includes('@')) { showMsg('regMsg', 'Adresse e-mail invalide.'); return; }
  }
  if (n === 3) {
    // Step 2 is optional fields, just proceed
  }
  goToStep(n);
}
function prevStep(n) { goToStep(n); }
function goToStep(n) {
  document.querySelectorAll('.reg-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.reg-step').forEach(d => { d.classList.remove('active','done'); });
  const panel = document.getElementById('reg-step-' + n);
  if (panel) panel.classList.add('active');
  for (let i = 1; i < n; i++) {
    const dot = document.getElementById('step-dot-' + i);
    if (dot) { dot.classList.add('done'); dot.innerHTML = '<i class="fa fa-check"></i>'; }
  }
  const cur = document.getElementById('step-dot-' + n);
  if (cur) cur.classList.add('active');
}

function handleRegister() {
  const pwd = document.getElementById('reg-pwd')?.value;
  const pwd2 = document.getElementById('reg-pwd2')?.value;
  if (!pwd || pwd.length < 6) { showMsg('regMsg', 'Mot de passe trop court (6 caractères min).'); return; }
  if (pwd !== pwd2) { showMsg('regMsg', 'Les mots de passe ne correspondent pas.'); return; }
  showMsg('regMsg', 'Compte créé avec succès ! Redirection…', 'success');
  setTimeout(() => { window.location.href = 'profil.html'; }, 1400);
}

// ── TAGS INPUT ──
const tagsData = { strengths: [], weaknesses: [] };
function addTag(event, type) {
  if (event.key !== 'Enter') return;
  event.preventDefault();
  const field = document.getElementById(type + '-field');
  const val = field.value.trim();
  if (!val || tagsData[type].includes(val)) { field.value = ''; return; }
  tagsData[type].push(val);
  renderTags(type);
  field.value = '';
}
function removeTag(type, val) {
  tagsData[type] = tagsData[type].filter(v => v !== val);
  renderTags(type);
}
function renderTags(type) {
  const list = document.getElementById(type + '-tags');
  if (!list) return;
  list.innerHTML = tagsData[type].map(v =>
    `<span class="badge-item">${v}<button onclick="removeTag('${type}','${v}')"><i class="fa fa-times"></i></button></span>`
  ).join('');
}

// ── MATCHING FILTER ──
const MOCK_MENTORS = [
  { id:1, name:'Ayodélé Koffi', filiere:'IA', niveau:'L3', role:'mentor', score:98, skills:['Python','Machine Learning','TensorFlow'], dispo:'Soir · Week-end', avatar:'img/a.jpg', format:'En ligne' },
  { id:2, name:'Rachida Bello', filiere:'GL', niveau:'L2', role:'mentor', score:91, skills:['Java','Git','Algo'], dispo:'Après-midi', avatar:'img/b.jpg', format:'Présentiel' },
  { id:3, name:'Kokou Mensah', filiere:'SI', niveau:'L3', role:'mentor', score:87, skills:['SQL','Django','Réseaux'], dispo:'Matin · Soir', avatar:'img/c.jpg', format:'Les deux' },
  { id:4, name:'Fatima Alabi', filiere:'SE&IoT', niveau:'L2', role:'mentoré', score:84, skills:['C','Arduino','Linux'], dispo:'Week-end', avatar:'img/d.jpg', format:'En ligne' },
  { id:5, name:'Razak Houessou', filiere:'IM', niveau:'L1', role:'mentoré', score:79, skills:['HTML','CSS','JS'], dispo:'Soir', avatar:'img/e.jpg', format:'Les deux' },
  { id:6, name:'Prudence Ahounto', filiere:'IA', niveau:'L2', role:'mentor', score:95, skills:['Python','Data Science','SQL'], dispo:'Matin · Week-end', avatar:'img/f.jpg', format:'En ligne' },
];

let filteredMentors = [...MOCK_MENTORS];
let currentType = 'mentor';

function setType(btn, type) {
  currentType = type;
  document.querySelectorAll('.toggle-group .toggle-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function applyFilters() {
  const matiere = document.getElementById('filterMatiere')?.value.toLowerCase() || '';
  const filiere = document.getElementById('filterFiliere')?.value || '';
  const niveau = document.getElementById('filterNiveau')?.value || '';
  filteredMentors = MOCK_MENTORS.filter(m => {
    const matchType = m.role === currentType;
    const matchMatiere = !matiere || m.skills.some(s => s.toLowerCase().includes(matiere));
    const matchFiliere = !filiere || m.filiere === filiere;
    const matchNiveau = !niveau || m.niveau === niveau;
    return matchType && matchMatiere && matchFiliere && matchNiveau;
  });
  renderMentorCards();
}

function resetFilters() {
  if (document.getElementById('filterMatiere')) document.getElementById('filterMatiere').value = '';
  if (document.getElementById('filterFiliere')) document.getElementById('filterFiliere').value = '';
  if (document.getElementById('filterNiveau')) document.getElementById('filterNiveau').value = '';
  filteredMentors = [...MOCK_MENTORS];
  renderMentorCards();
}

function sortResults(by) {
  if (by === 'score') filteredMentors.sort((a,b) => b.score - a.score);
  else if (by === 'filiere') filteredMentors.sort((a,b) => a.filiere.localeCompare(b.filiere));
  else if (by === 'niveau') filteredMentors.sort((a,b) => a.niveau.localeCompare(b.niveau));
  renderMentorCards();
}

let userPosts = [];
let selectedPublishType = 'offre';

function renderMentorCards() {
  const container = document.getElementById('mentorCards');
  const count = document.getElementById('results-count');
  if (!container) return;
  if (count) count.textContent = filteredMentors.length + ' profil' + (filteredMentors.length > 1 ? 's' : '') + ' trouvé' + (filteredMentors.length > 1 ? 's' : '');
  if (filteredMentors.length === 0) {
    container.innerHTML = '<p style="color:var(--gray);padding:32px;">Aucun profil ne correspond à ta recherche.</p>';
    return;
  }
  container.innerHTML = filteredMentors.map(m => `
    <div class="mentor-card-item" onclick="openConvFromMatch(${m.id})">
      <span class="mc-type-badge ${m.role}">${m.role === 'mentor' ? '<i class="fa fa-star"></i> Mentor' : '<i class="fa fa-user"></i> Mentoré'}</span>
      <div class="mc-header">
        <img src="${m.avatar}" alt="${m.name}" class="mc-avatar"/>
        <div class="mc-info">
          <h4 class="mc-name">${m.name}</h4>
          <p class="mc-meta">${m.filiere} · ${m.niveau}</p>
        </div>
        <span class="mc-score">${m.score}%</span>
      </div>
      <div class="mc-tags">${m.skills.map(s => `<span>${s}</span>`).join('')}</div>
      <p class="mc-dispo"><i class="fa fa-clock"></i> ${m.dispo} · ${m.format}</p>
      <div class="mc-actions">
        <button class="btn-primary" onclick="event.stopPropagation();openConvFromMatch(${m.id})"><i class="fa fa-comment"></i> Contacter</button>
        <button class="btn-ghost" onclick="event.stopPropagation();">Profil</button>
      </div>
    </div>
  `).join('');
}

function setPublishType(btn, type) {
  selectedPublishType = type;
  document.querySelectorAll('#offerModal .toggle-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
}

function publishOfferOrDemand() {
  const type = selectedPublishType;
  const title = document.getElementById('post-title')?.value.trim();
  const details = document.getElementById('post-details')?.value.trim();
  const dispo = document.getElementById('post-dispo')?.value.trim();
  const format = document.getElementById('post-format')?.value;
  if (!title || !details) {
    showMsg('offerMsg', 'Donne un titre et une description pour ta demande.');
    return;
  }
  const post = {
    id: Date.now(),
    type,
    title,
    details,
    dispo,
    format,
    createdAt: new Date().toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }),
    status: type === 'demande' ? 'En attente' : 'Publiée',
  };
  userPosts.unshift(post);
  renderUserPosts();
  if (type === 'demande') {
    showMsg('offerMsg', 'Demande publiée ! Un mentor intéressé te contactera bientôt.', 'success');
    simulateInterest(post);
  } else {
    showMsg('offerMsg', 'Offre publiée ! Elle est visible sur ta page profil.', 'success');
  }
  setTimeout(() => closeModal('offerModal'), 1200);
  document.getElementById('post-title').value = '';
  document.getElementById('post-details').value = '';
  document.getElementById('post-dispo').value = '';
  document.getElementById('post-format').value = 'Présentiel';
}

function renderUserPosts() {
  const container = document.getElementById('offersList');
  if (!container) return;
  if (userPosts.length === 0) {
    container.innerHTML = '<p class="empty-note">Aucune offre ou demande publiée pour le moment.</p>';
    return;
  }
  container.innerHTML = userPosts.map(post => `
    <div class="post-item">
      <span class="post-type ${post.type}">${post.type === 'demande' ? 'Demande' : 'Offre'}</span>
      <div>
        <p><strong>${post.title}</strong></p>
        <p class="post-meta">${post.details} · ${post.dispo || 'Aucune dispo précisée'} · ${post.format}</p>
        <p class="post-status">${post.status}</p>
      </div>
      <button class="post-del" title="Supprimer" onclick="removePost(${post.id})"><i class="fa fa-times"></i></button>
    </div>
  `).join('');
}

function removePost(id) {
  userPosts = userPosts.filter(post => post.id !== id);
  renderUserPosts();
}

function simulateInterest(post) {
  setTimeout(() => {
    const candidate = MOCK_MENTORS.find(m => m.role === 'mentor') || MOCK_MENTORS[0];
    const conv = MOCK_CONVS.find(c => c.id === candidate.id);
    const welcome = `Bonjour ! Je vois que tu recherches ${post.title}. Je peux t'aider, on en discute ?`;
    const time = new Date().getHours() + ':' + String(new Date().getMinutes()).padStart(2, '0');
    if (conv) {
      conv.messages.push({ from:'them', text:welcome, time });
      conv.lastMsg = welcome;
      conv.time = time;
      conv.unread += 1;
    } else {
      MOCK_CONVS.unshift({
        id: candidate.id,
        name: candidate.name,
        role: `${candidate.role === 'mentor' ? 'Mentor' : 'Mentoré'} · ${candidate.filiere} · ${candidate.niveau}`,
        avatar: candidate.avatar,
        unread: 1,
        lastMsg: welcome,
        time,
        messages: [
          { from:'them', text:welcome, time }
        ]
      });
    }
    const postIndex = userPosts.findIndex(p => p.id === post.id);
    if (postIndex !== -1) {
      userPosts[postIndex].status = `Intérêt reçu de ${candidate.name}`;
    }
    renderUserPosts();
    renderConvList();
  }, 2500);
}

function openConvFromMatch(id) {
  const m = MOCK_MENTORS.find(x => x.id === id);
  if (!m) return;
  localStorage.setItem('openConvId', id);
  window.location.href = 'discussions.html';
}

// ── MESSAGING ──
const MOCK_CONVS = [
  { id:1, name:'Ayodélé Koffi', role:'Mentor · IA · L3', avatar:'img/a.jpg', unread:1, lastMsg:'Oui, je suis dispo ce soir !', time:'14:32',
    messages:[
      { from:'them', text:'Salut ! J\'ai vu ton profil. Tu cherches de l\'aide en Python ?', time:'14:20' },
      { from:'me', text:'Oui exactement ! Je bloque sur les générateurs et les décorateurs.', time:'14:22' },
      { from:'them', text:'Pas de souci, c\'est mon domaine. Tu veux qu\'on organise une session ?', time:'14:25' },
      { from:'me', text:'Oui, quand es-tu disponible ?', time:'14:28' },
      { from:'them', text:'Oui, je suis dispo ce soir !', time:'14:32' },
    ]
  },
  { id:2, name:'Rachida Bello', role:'Mentor · GL · L2', avatar:'img/b.jpg', unread:1, lastMsg:'Je t\'envoie les ressources.', time:'11:05',
    messages:[
      { from:'them', text:'Bonjour ! J\'ai vu que tu as besoin d\'aide en SQL.', time:'10:50' },
      { from:'me', text:'Oui, les jointures complexes surtout.', time:'10:52' },
      { from:'them', text:'Je t\'envoie les ressources.', time:'11:05' },
    ]
  },
  { id:3, name:'Razak Houessou', role:'Mentoré · IM · L1', avatar:'img/e.jpg', unread:0, lastMsg:'Merci beaucoup !', time:'Hier',
    messages:[
      { from:'me', text:'Tu as des questions sur le cours d\'Algo ?', time:'Hier 16:00' },
      { from:'them', text:'Oui ! Les récursions je comprends pas trop.', time:'Hier 16:05' },
      { from:'me', text:'Voilà un exemple concret avec la factorielle…', time:'Hier 16:10' },
      { from:'them', text:'Merci beaucoup !', time:'Hier 16:30' },
    ]
  },
];

let activeConvId = null;

function renderConvList(filter='') {
  const container = document.getElementById('convItems');
  if (!container) return;
  const filtered = MOCK_CONVS.filter(c => c.name.toLowerCase().includes(filter.toLowerCase()));
  container.innerHTML = filtered.map(c => `
    <div class="conv-item ${activeConvId === c.id ? 'active' : ''}" onclick="openConv(${c.id})">
      <img src="${c.avatar}" alt="${c.name}"/>
      <div class="conv-item-info">
        <p class="conv-item-name">${c.name}</p>
        <p class="conv-item-preview">${c.lastMsg}</p>
      </div>
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px;">
        <span class="conv-item-time">${c.time}</span>
        ${c.unread > 0 ? `<span class="conv-unread">${c.unread}</span>` : ''}
      </div>
    </div>
  `).join('');
  const totalUnread = document.getElementById('totalUnread');
  if (totalUnread) totalUnread.textContent = MOCK_CONVS.reduce((sum,c) => sum + c.unread, 0);
}

function filterConvs(val) { renderConvList(val); }

function openConv(id) {
  activeConvId = id;
  const conv = MOCK_CONVS.find(c => c.id === id);
  if (!conv) return;
  conv.unread = 0;
  const totalUnread = document.getElementById('totalUnread');
  if (totalUnread) totalUnread.textContent = MOCK_CONVS.reduce((s,c)=>s+c.unread,0);
  document.getElementById('chatEmpty').style.display = 'none';
  document.getElementById('chatWindow').style.display = 'flex';
  document.getElementById('chat-name').textContent = conv.name;
  document.getElementById('chat-role').textContent = conv.role;
  document.getElementById('chat-avatar').src = conv.avatar;
  renderConvList();
  renderMessages(conv);

  // Mobile: hide conv list
  if (window.innerWidth <= 900) {
    document.getElementById('convList').style.display = 'none';
    document.getElementById('chatArea').style.flex = '1';
  }
}

function backToList() {
  document.getElementById('convList').style.display = '';
  document.getElementById('chatWindow').style.display = 'none';
  document.getElementById('chatEmpty').style.display = 'flex';
  activeConvId = null;
}

function renderMessages(conv) {
  const container = document.getElementById('chatMessages');
  if (!container) return;
  container.innerHTML = conv.messages.map(m => `
    <div class="msg-bubble ${m.from}">
      ${m.text}
      <div class="msg-meta">${m.time}</div>
    </div>
  `).join('');
  container.scrollTop = container.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById('msgInput');
  if (!input || !activeConvId) return;
  const text = input.value.trim();
  if (!text) return;
  const conv = MOCK_CONVS.find(c => c.id === activeConvId);
  if (!conv) return;
  const now = new Date();
  const time = now.getHours() + ':' + String(now.getMinutes()).padStart(2,'0');
  conv.messages.push({ from:'me', text, time });
  conv.lastMsg = text;
  conv.time = time;
  input.value = '';
  renderMessages(conv);
  renderConvList();

  // Simulate response after 1.5s
  setTimeout(() => {
    const responses = [
      'D\'accord, je vois !', 'Bonne question.', 'On peut prévoir ça pour demain ?',
      'Super, je vais préparer ça.', 'Merci pour l\'info !', 'Voilà, c\'est clair maintenant.'
    ];
    const reply = responses[Math.floor(Math.random() * responses.length)];
    const t2 = new Date();
    const t2str = t2.getHours() + ':' + String(t2.getMinutes()).padStart(2,'0');
    conv.messages.push({ from:'them', text:reply, time:t2str });
    conv.lastMsg = reply;
    conv.time = t2str;
    if (activeConvId === conv.id) renderMessages(conv);
    renderConvList();
  }, 1500);
}

// ── PROFILE EDIT ──
let editMode = false;
function toggleEdit() {
  editMode = !editMode;
  const fields = ['edit-prenom','edit-nom','edit-email','edit-tel','edit-filiere','edit-niveau','edit-bio'];
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.disabled = !editMode;
  });
  const saveRow = document.getElementById('save-row');
  const editBtn = document.getElementById('editBtn');
  if (saveRow) saveRow.style.display = editMode ? 'flex' : 'none';
  if (editBtn) editBtn.innerHTML = editMode ? '<i class="fa fa-times"></i> Annuler' : '<i class="fa fa-edit"></i> Modifier';
}
function cancelEdit() {
  editMode = true; toggleEdit();
}
function saveProfile() {
  const prenom = document.getElementById('edit-prenom')?.value.trim();
  const nom = document.getElementById('edit-nom')?.value.trim();
  const filiere = document.getElementById('edit-filiere')?.value;
  const niveau = document.getElementById('edit-niveau')?.value;
  const bio = document.getElementById('edit-bio')?.value.trim();
  if (!prenom || !nom) { showMsg('profMsg','Prénom et nom requis.'); return; }
  const nameEl = document.getElementById('prof-name');
  const subEl = document.getElementById('prof-filiere-niveau');
  const bioEl = document.getElementById('prof-bio');
  if (nameEl) nameEl.textContent = prenom + ' ' + nom;
  if (subEl) subEl.textContent = filiere + ' · ' + niveau;
  if (bioEl && bio) bioEl.textContent = bio;
  editMode = true; toggleEdit();
  showMsg('profMsg','Profil mis à jour avec succès.','success');
}
function previewAvatar(input) {
  if (!input.files || !input.files[0]) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    const img = document.getElementById('prof-avatar');
    if (img) img.src = e.target.result;
  };
  reader.readAsDataURL(input.files[0]);
}
function handleLogout() { window.location.href = 'index.html'; }

// ── INIT ──
document.addEventListener('DOMContentLoaded', () => {
  // Matching page
  if (document.getElementById('mentorCards')) {
    renderMentorCards();
  }
  // Messaging page
  if (document.getElementById('convItems')) {
    renderConvList();
    const savedId = localStorage.getItem('openConvId');
    if (savedId) { openConv(parseInt(savedId)); localStorage.removeItem('openConvId'); }
  }
  // Profile requests / offers
  if (document.getElementById('offersList')) {
    renderUserPosts();
  }
});

// 🌐 URL de base de ton backend Django
const API_URL = "https://onrender.com";


// ==========================================
// 🔐 1. GESTION DE L'AUTHENTIFICATION
// ==========================================

// Fonction pour s'inscrire (Page enregistrer.html)
async function inscription(event) {
    event.preventDefault();
    
    const nom = document.getElementById("nom")?.value;
    const email = document.getElementById("email")?.value;
    const password = document.getElementById("password")?.value;
    const role = document.getElementById("role")?.value; // Recueille 'mentor', 'mentore' ou 'les_deux'

    try {
        const response = await fetch(`${API_URL}/api/auth/register/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nom, email, password, role })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Inscription réussie ! Connectez-vous.");
            window.location.href = "connexion.html";
        } else {
            alert("Erreur d'inscription : " + (data.error || "Vérifiez vos informations"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Impossible de contacter le serveur backend.");
    }
}

// Fonction pour se connecter (Page connexion.html)
async function connexion(event) {
    event.preventDefault();

    const email = document.getElementById("email")?.value;
    const password = document.getElementById("password")?.value;

    try {
        const response = await fetch(`${API_URL}/api/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.token) {
            localStorage.setItem("token", data.token);
            alert("Connexion réussie !");
            window.location.href = "index.html";
        } else {
            alert("Erreur : " + (data.error || "Identifiants incorrects"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Impossible de contacter le serveur backend.");
    }
}

// ==========================================
// 🛠️ 2. REQUÊTES SÉCURISÉES & PROFILS (NOUVEAU)
// ==========================================

function getHeaders() {
    const token = localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

function deconnexion() {
    localStorage.removeItem("token");
    alert("Vous avez été déconnecté.");
    window.location.href = "connexion.html";
}
// Remplace l'ancienne fonction chargerProfil dans ton app.js par celle-ci :
async function chargerProfil() {
    try {
        const response = await fetch(`${API_URL}/api/profil/`, {
            method: "GET",
            headers: getHeaders()
        });
        const user = await response.json();

        if (response.ok) {
            // 🚨 Correction des IDs pour correspondre exactement à ton profil.html !
            if (document.getElementById("prof-name")) {
                document.getElementById("prof-name").innerText = user.nom;
            }
            if (document.getElementById("edit-nom")) {
                document.getElementById("edit-nom").value = user.nom;
            }
            if (document.getElementById("edit-email")) {
                document.getElementById("edit-email").value = user.email;
            }
            
            // Gère l'affichage du rôle ou badge s'il existe
            const zoneSub = document.getElementById("prof-filiere-niveau");
            if (zoneSub && user.role) {
                if (user.role === "les_deux") {
                    zoneSub.innerText = "Mentor & Mentoré";
                } else if (user.role === "mentor") {
                    zoneSub.innerText = "Mentor (Guide)";
                } else {
                    zoneSub.innerText = "Mentoré (Élève)";
                }
            }
        }
    } catch (error) {
        console.error("Erreur lors du chargement du profil :", error);
    }
}

// 🚨 Ajoute cette fonction pour gérer le bouton de déconnexion d'Adrien
function handleLogout() {
    localStorage.removeItem("token");
    alert("Vous avez été déconnecté.");
    window.location.href = "login.html"; // Redirige vers la page d'Adrien
}


// ==========================================
// 📅 3. GESTION DES DISPONIBILITÉS (MIGRATION)
// ==========================================

// Envoie un créneau pour un mentoré (Table disponibilites_mentores)
async function ajouterDispoMentore(event) {
    event.preventDefault();
    
    const jour = document.getElementById("dispo-jour").value; // Ex: 'Lundi'
    const heure_debut = document.getElementById("dispo-debut").value; // Ex: '14:00'
    const heure_fin = document.getElementById("dispo-fin").value; // Ex: '16:00'

    try {
        const response = await fetch(`${API_URL}/api/disponibilites-mentores/`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({ jour, heure_debut, heure_fin })
        });

        if (response.ok) {
            alert("Disponibilité de mentoré enregistrée avec succès !");
            // Optionnel : recharger la liste des dispos affichées
        } else {
            alert("Erreur lors de l'enregistrement du créneau.");
        }
    } catch (error) {
        console.error("Erreur :", error);
    }
}

// ==========================================
// ⚡ 4. ÉCOUTEURS D'ÉVÉNEMENTS (DÉMARRAGE)
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    // Formulaires d'authentification
    const formInscription = document.getElementById("form-inscription");
    if (formInscription) formInscription.addEventListener("submit", inscription);

    const formConnexion = document.getElementById("form-connexion");
    if (formConnexion) formConnexion.addEventListener("submit", connexion);

    // Formulaire de disponibilité mentoré (s'il existe sur la page actuelle)
    const formDispoMentore = document.getElementById("form-dispo-mentore");
    if (formDispoMentore) formDispoMentore.addEventListener("submit", ajouterDispoMentore);

    // Si on est sur la page profil, charger automatiquement les données
    if (window.location.pathname.includes("profil.html")) {
        chargerProfil();
    }
});
