import base64
import os
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# --- FONCTION SECURISEE POUR CHARGER LA PHOTO ---
def charger_image_locale(nom_fichier):
    dossier_actuel = os.path.dirname(__file__)
    chemin_complet = os.path.join(dossier_actuel, nom_fichier)
    
    with open(chemin_complet, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="Mon Minuteur", page_icon="⏳")

# --- IMAGE DE FOND PERSONNELLE ET STYLE ---
nom_fichier_photo = "ma_photo.jpg"

try:
    img_b64 = charger_image_locale(nom_fichier_photo)
    url_image_fond = f"data:image/jpeg;base64,{img_b64}"
except Exception as e:
    url_image_fond = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80"

st.markdown(
    f"""
    <style>
    /* Image de fond */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url("{url_image_fond}");
        background-size: contain;
        background-position: center top;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #1a1a1a;
    }}
    
    h1, h2, h3 {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
    }}

    /* Encadrement du bloc metric (Heures / Minutes / Secondes) - ROUGE */
    div[data-testid="stMetric"] {{
        background-color: #dc2626 !important;
        padding: 15px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3) !important;
    }}
    
    /* Textes dans le bloc metric en blanc */
    div[data-testid="stMetric"] * {{
        color: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TEXTES DE LA PAGE ---
st.title("Alea iacta est")
st.subheader("Le compte à rebours est lancé !")

# --- MINUTEUR 1 : HTML/JS (JOURS, HEURES, MINUTES, SECONDES) ---
code_html_js = """
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

<div style="text-align: center; margin-bottom: 15px;" id="zone-bouton-musique">
    <button id="bouton-musique" style="padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 8px; border: none; background-color: #dc2626; color: white; box-shadow: 1px 1px 5px rgba(0,0,0,0.3); font-weight: bold;">
        🎵 Activer la musique d'attente
    </button>
</div>

<!-- Boîte du minuteur sur fond ROUGE avec texte BLANC -->
<div id="minuteur" style="text-align: center; font-size: 50px; font-weight: bold; color: #ffffff !important; background-color: #dc2626 !important; padding: 30px; border-radius: 15px; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.4);">
    Chargement...
</div>

<script>
    const dateCible = new Date("2026-10-02T12:15:00").getTime();
    let confettisLances = false;

    // Musique calme (Erik Satie)
    const musiqueAttente = new Audio("https://upload.wikimedia.org/wikipedia/commons/4/4e/Erik_Satie_-_Gymnop%C3%A9die_No._1.ogg");
    musiqueAttente.loop = true; 
    
    const musiqueVictoire = new Audio("https://actions.google.com/sounds/v1/crowds/crowd_cheering.ogg");

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
            boutonMusique.style.backgroundColor = "#dc2626";
            musiqueEnCours = false;
        }
    });

    const intervalle = setInterval(function() {
        const maintenant = new Date().getTime();
        const difference = dateCible - maintenant;

        if (difference <= 0) {
            clearInterval(intervalle);
            document.getElementById("minuteur").innerHTML = "⏰ Temps écoulé !";
            
            if (!confettisLances) {
                musiqueAttente.pause();
                document.getElementById("zone-bouton-musique").style.display = "none";
                musiqueVictoire.play().catch(function(error) { console.log("Audio bloqué."); });

                confetti({ particleCount: 150, spread: 100, origin: { y: 0.1 } });
                setTimeout(() => { confetti({ particleCount: 150, spread: 120, origin: { y: 0.3 } }); }, 500);
                confettisLances = true;
            }
            return;
        }

        // Calcul : Jours, Heures, Minutes, Secondes
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

# --- MINUTEUR 2 : CALCUL PYTHON (HEURES, MINUTES, SECONDES TOTALES) ---
maintenant = datetime.now()
date_cible = datetime(2026, 10, 2, 12, 15)

if maintenant < date_cible:
    difference = date_cible - maintenant
    total_secondes = int(difference.total_seconds())
    
    heures_totales = total_secondes // 3600
    minutes = (total_secondes % 3600) // 60
    secondes = total_secondes % 60
    
    st.metric(
        label="⏳ Temps total restant",
        value=f"{heures_totales}h {minutes:02d}m {secondes:02d}s",
        help="Nombre total d'heures, minutes et secondes restantes.",
    )
else:
    st.info("La date cible est atteinte ou dépassée !")
    st.balloons()
