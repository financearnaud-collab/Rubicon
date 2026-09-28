import base64
from datetime import date, timedelta
import streamlit as st
import streamlit.components.v1 as components

# --- FONCTION POUR CHARGER LA PHOTO ---
def charger_image_locale(chemin_image):
    with open(chemin_image, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="Mon Minuteur", page_icon="⏳")

# --- IMAGE DE FOND PERSONNELLE ET STYLE ---
# Mets ici le nom exact de ta photo (elle doit être dans le même dossier que ce script)
nom_fichier_photo = "ma_photo.jpg"

try:
    img_b64 = charger_image_locale(nom_fichier_photo)
    # Si c'est un PNG, remplace 'jpeg' par 'png' ci-dessous
    url_image_fond = f"data:image/jpeg;base64,{img_b64}"
except FileNotFoundError:
    # Image de secours si ton fichier photo n'est pas trouvé
    url_image_fond = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80"

st.markdown(
    f"""
    <style>
    /* Image de fond ajustée pour s'afficher en entier */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url("{url_image_fond}");
        background-size: contain; /* Affiche 100% de l'image sans la rogner */
        background-position: center top; /* Place l'image en haut au centre */
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #1a1a1a; /* Fond gris foncé sur les côtés si la photo ne remplit pas l'écran */
    }}
    
    /* Titres et sous-titres en blanc net avec ombre portée */
    h1, h2, h3 {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
    }}

    /* Encadrement du bloc metric (Jours travaillés) en rose pâle */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 228, 230, 0.92);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }}
    [data-testid="stMetricLabel"] p {{
        color: #881337 !important;
        font-weight: 600 !important;
    }}
    [data-testid="stMetricValue"] div {{
        color: #4c0519 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TEXTES DE LA PAGE ---
st.title("Alea iacta est")
st.subheader("5 jours... Putain, c'est long !")

# --- MINUTEUR HTML/JS ---
code_html_js = """
<!-- Importation de la bibliothèque de confettis -->
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

<!-- Zone du bouton pour la musique d'attente -->
<div style="text-align: center; margin-bottom: 15px;" id="zone-bouton-musique">
    <button id="bouton-musique" style="padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 8px; border: none; background-color: #ff4b4b; color: white; box-shadow: 1px 1px 5px rgba(0,0,0,0.3); font-weight: bold;">
        🎵 Activer la musique d'attente
    </button>
</div>

<!-- Boîte du minuteur sur fond rose pâle -->
<div id="minuteur" style="text-align: center; font-size: 50px; font-weight: bold; color: #4c0519; background-color: rgba(255, 228, 230, 0.95); padding: 30px; border-radius: 15px; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.4);">
    Chargement...
</div>

<script>
    const dateCible = new Date("2026-10-30T16:15:00").getTime();
    let confettisLances = false;

    // --- PRÉPARATION DES MUSIQUES ---
    const musiqueAttente = new Audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3");
    musiqueAttente.loop = true; 
    
    const musiqueVictoire = new Audio("https://actions.google.com/sounds/v1/crowds/crowd_cheering.ogg");

    // --- GESTION DU BOUTON MUSIQUE D'ATTENTE ---
    let musiqueEnCours = false;
    const boutonMusique = document.getElementById("bouton-musique");
    
    boutonMusique.addEventListener("click", function() {
        if (!musiqueEnCours) {
            musiqueAttente.play();
            boutonMusique.innerHTML = "🔇 Couper la musique d'attente";
            boutonMusique.style.backgroundColor = "#1f77b4";
            musiqueEnCours = true;
        } else {
            musiqueAttente.pause();
            boutonMusique.innerHTML = "🎵 Activer la musique d'attente";
            boutonMusique.style.backgroundColor = "#ff4b4b";
            musiqueEnCours = false;
        }
    });

    // --- COMPTE À REBOURS ---
    const intervalle = setInterval(function() {
        const maintenant = new Date().getTime();
        const difference = dateCible - maintenant;

        if (difference <= 0) {
            clearInterval(intervalle);
            document.getElementById("minuteur").innerHTML = "⏰ Temps écoulé !";
            
            if (!confettisLances) {
                musiqueAttente.pause();
                document.getElementById("zone-bouton-musique").style.display = "none";

                musiqueVictoire.play().catch(function(error) {
                    console.log("Le navigateur a bloqué la lecture audio.");
                });

                confetti({
                    particleCount: 150,
                    spread: 100,
                    origin: { y: 0.1 }
                });
                
                setTimeout(() => {
                    confetti({
                        particleCount: 150,
                        spread: 120,
                        origin: { y: 0.3 }
                    });
                }, 500);

                confettisLances = true;
            }
            return;
        }

        const jours = Math.floor(difference / (1000 * 60 * 60 * 24));
        let heures = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        let secondes = Math.floor((difference % (1000 * 60)) / 1000);

        heures = heures < 10 ? "0" + heures : heures;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        secondes = secondes < 10 ? "0" + secondes : secondes;

        document.getElementById("minuteur").innerHTML = jours + " Jours <br>" + heures + " : " + minutes + " : " + secondes;
    }, 1000);
</script>
"""

components.html(code_html_js, height=380)

# --- CALCUL DES JOURS OUVRÉS ---
def calculer_jours_ouvres(debut: date, fin: date) -> int:
    jours_ouvres = 0
    actuel = debut
    while actuel < fin:
        if actuel.weekday() < 5:  # Du lundi (0) au vendredi (4)
            jours_ouvres += 1
        actuel += timedelta(days=1)
    return jours_ouvres

aujourdhui = date.today()
date_cible = date(2026, 10, 30)

if aujourdhui < date_cible:
    nb_jours_ouvres = calculer_jours_ouvres(aujourdhui, date_cible)
    st.metric(
        label="💼 Jours travaillés restants",
        value=f"{nb_jours_ouvres} jours",
        help="Nombre de jours ouvrés hors week-ends entre aujourd'hui et la date cible.",
    )
else:
    st.info("La date cible est atteinte ou dépassée !")
    st.balloons()