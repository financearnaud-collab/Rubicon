import base64
import os
import streamlit as st
import streamlit.components.v1 as components

# --- FONCTION SÉCURISÉE POUR CHARGER LA PHOTO ---
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
except Exception:
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
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TEXTES DE LA PAGE ---
st.title("Alea iacta est")
st.subheader("Le compte à rebours est lancé !")

# --- COMPOSANT HTML/JS AVEC LES 2 MINUTEURS EN DIRECT ---
code_html_js = """
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

<!-- Bouton Musique -->
<div style="text-align: center; margin-bottom: 20px;" id="zone-bouton-musique">
    <button id="bouton-musique" style="padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 8px; border: none; background-color: #dc2626; color: white; box-shadow: 1px 1px 5px rgba(0,0,0,0.3); font-weight: bold;">
        🎵 Activer la musique d'attente
    </button>
</div>

<!-- MINUTEUR 1 : Jours, Heures, Minutes, Secondes -->
<div id="minuteur1" style="text-align: center; font-size: 45px; font-weight: bold; color: #ffffff !important; background-color: #dc2626 !important; padding: 25px; border-radius: 15px; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.4); margin-bottom: 20px;">
    Chargement...
</div>

<!-- MINUTEUR 2 : Total Heures, Minutes, Secondes -->
<div id="minuteur2" style="text-align: center; font-size: 26px; font-weight: bold; color: #ffffff !important; background-color: #dc2626 !important; padding: 15px; border-radius: 12px; font-family: sans-serif; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);">
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
            document.getElementById("minuteur1").innerHTML = "⏰ Temps écoulé !";
            document.getElementById("minuteur2").innerHTML = "🎉 C'est fini !";
            
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

        // --- CALCUL MINUTEUR 1 (Jours, Heures, Minutes, Secondes) ---
        const jours = Math.floor(difference / (1000 * 60 * 60 * 24));
        let heures = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        let secondes = Math.floor((difference % (1000 * 60)) / 1000);

        let hStr = heures < 10 ? "0" + heures : heures;
        let mStr = minutes < 10 ? "0" + minutes : minutes;
        let sStr = secondes < 10 ? "0" + secondes : secondes;

        document.getElementById("minuteur1").innerHTML = jours + " Jours <br>" + hStr + " : " + mStr + " : " + sStr;

        // --- CALCUL MINUTEUR 2 (Heures Totales, Minutes, Secondes) ---
        const heuresTotales = Math.floor(difference / (1000 * 60 * 60));
        
        document.getElementById("minuteur2").innerHTML = "⏳ Temps total : " + heuresTotales + "h " + mStr + "m " + sStr + "s";
    }, 1000);
</script>
"""

components.html(code_html_js, height=480)
