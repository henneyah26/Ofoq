# === À COLLER dans app.py : remplace HERO_VIDEO_URL + LOGIN_CSS (section 4) ===
HERO_VIDEO_URL = "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_091828_e240eb17-6edc-4129-ad9d-98678e3fd238.mp4"

# Slogan affiché en bas à gauche de la PAGE (injecté dans <body>, jamais dans la carte)
LOGIN_SLOGAN_HTML = ('<i></i><b>Le ciel du Maroc,<br>en chiffres.</b>'
                     '<span>Suivez le trafic aérien, année après année.</span>')

# Empilement : vidéo 0 < voile 1 < slogan 2 < carte 3.
# Les calques sont des enfants de <body> (voir LOGIN_BG_JS) : aucun ancêtre avec backdrop-filter / transform
# ne peut donc les piéger, et leur « position:fixed » se rapporte bien à la fenêtre.
LOGIN_CSS = """
<style>
/* Page : fond de secours pendant le chargement de la vidéo, header et barre latérale masqués */
html,body{background:#0A1440!important}
.stApp,[data-testid="stApp"],[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]{display:none!important}
/* Calques plein écran créés par le script (masqués par défaut, affichés seulement tant que cette feuille existe) */
#ofoq-bg{display:block!important}
#ofoq-bg .ofoq-video{position:fixed;top:0;left:0;width:100vw;height:100vh;height:100dvh;object-fit:cover;z-index:0;background:#0A1440;pointer-events:none}
#ofoq-bg .ofoq-veil{position:fixed;top:0;left:0;width:100vw;height:100vh;height:100dvh;z-index:1;background:rgba(11,42,107,.4);pointer-events:none}
#ofoq-bg .ofoq-slogan{position:fixed;left:48px;bottom:44px;z-index:2;max-width:420px;color:#fff;pointer-events:none;
  font-family:'DM Sans',sans-serif;text-shadow:0 2px 14px rgba(5,15,50,.65),0 1px 3px rgba(5,15,50,.55)}
#ofoq-bg .ofoq-slogan i{display:block;width:44px;height:4px;border-radius:4px;background:#ED2939;margin-bottom:14px}
#ofoq-bg .ofoq-slogan b{display:block;font:700 34px/1.15 'Sora',sans-serif;margin-bottom:8px}
#ofoq-bg .ofoq-slogan span{font-size:15px;color:#fff}
/* Centrage : stMain devient un conteneur flex, les marges auto centrent la carte (H + V, sans coupure si l'écran est bas) */
[data-testid="stMain"]{display:flex!important;flex-direction:column!important;min-height:100vh;min-height:100dvh;padding:1rem!important;box-sizing:border-box}
/* Carte : opaque, au-dessus de tout, sans backdrop-filter ni transform (ils piégeraient les éléments fixed) */
.block-container,[data-testid="stMainBlockContainer"]{position:relative!important;z-index:3;box-sizing:border-box;
  width:min(440px,100% - 2rem)!important;max-width:440px!important;margin:auto!important;padding:1.4rem 1.7rem 1.6rem!important;
  background:rgba(255,255,255,.96)!important;border-radius:20px;border:1px solid rgba(255,255,255,.7);
  box-shadow:0 18px 50px rgba(5,15,50,.35),0 4px 0 #ED2939;color:#0B1F4D;
  backdrop-filter:none!important;-webkit-backdrop-filter:none!important;filter:none!important;transform:none!important}
.block-container .login-head{padding:6px 0 8px;margin:0}
.block-container .login-head h1{color:#0B2A6B}
.block-container .login-head p{color:#4A5B85}
.block-container [data-testid="stForm"]{border:none;padding:.4rem 0 0;background:transparent}
.block-container [data-testid="stTabs"] [data-baseweb="tab-list"]{justify-content:center}
.block-container [data-baseweb="tab"]{color:#4A5B85}
.block-container [aria-selected="true"]{color:#ED2939}
.block-container [data-testid="stWidgetLabel"] p{color:#0B2A6B;font-weight:500}
.block-container [data-baseweb="input"],.block-container [data-baseweb="base-input"]{background:#F4F5FA;border-radius:10px}
.block-container input{color:#0B1F4D}
/* L'iframe du script (hauteur 0) ne doit pas créer d'espace dans la carte */
.block-container [data-testid="stElementContainer"]:has(> iframe[height="0"]),
.block-container [data-testid="stElementContainer"]:has(iframe[height="0"]){position:absolute;width:0;height:0;overflow:hidden;margin:0}
@media (max-width:1100px){#ofoq-bg .ofoq-slogan{display:none}}
@media (max-width:560px){[data-testid="stMain"]{padding:.6rem!important}
  .block-container,[data-testid="stMainBlockContainer"]{width:calc(100% - 1.2rem)!important;padding:1.1rem 1rem 1.2rem!important}}
</style>
"""

# Script exécuté dans l'iframe components.html (hauteur 0) : il crée vidéo + voile + slogan dans le <body> du
# document PARENT. Idempotent : un rerun Streamlit ne recrée rien et ne relance pas la vidéo.
LOGIN_BG_JS = """
<script>
(function () {
  var d; try { d = window.parent.document; } catch (e) { return; }
  var root = d.getElementById('ofoq-bg');
  if (!root) {
    root = d.createElement('div');
    root.id = 'ofoq-bg';
    root.setAttribute('aria-hidden', 'true');
    root.style.display = 'none';              // affiché uniquement par LOGIN_CSS (#ofoq-bg{display:block!important})
    var v = d.createElement('video');
    v.className = 'ofoq-video';
    v.src = __VIDEO_URL__;
    v.preload = 'auto';
    root.appendChild(v);
    var veil = d.createElement('div'); veil.className = 'ofoq-veil'; root.appendChild(veil);
    var tx = d.createElement('div'); tx.className = 'ofoq-slogan'; tx.innerHTML = __SLOGAN__; root.appendChild(tx);
    d.body.appendChild(root);
  }
  var vid = root.querySelector('video');
  if (!vid) return;
  // « muted » doit être posé en propriété JS (l'attribut seul est ignoré sur un élément créé dynamiquement)
  vid.muted = true; vid.defaultMuted = true; vid.autoplay = true; vid.loop = true;
  vid.playsInline = true; vid.setAttribute('playsinline', ''); vid.setAttribute('muted', '');
  var go = function () { try { var p = vid.play(); if (p && p.catch) p.catch(function () {}); } catch (e) {} };
  go();
  vid.addEventListener('canplay', go);
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {   // filet de sécurité si l'autoplay est bloqué
    d.addEventListener(ev, go, { once: true, passive: true });
  });
})();
</script>
""".replace("__VIDEO_URL__", json.dumps(HERO_VIDEO_URL)).replace("__SLOGAN__", json.dumps(LOGIN_SLOGAN_HTML))

# À appeler dès que la personne est connectée : retire les calques du <body> (ils survivent aux reruns)
NETTOYER_FOND_JS = ("<script>try{var e=window.parent.document.getElementById('ofoq-bg');"
                    "if(e){var v=e.querySelector('video');if(v){v.pause();v.removeAttribute('src');v.load();}e.remove();}}"
                    "catch(err){}</script>")


# === À COLLER dans app.py : remplace page_connexion() ===
def page_connexion() -> None:
    """Première page : vidéo plein écran en arrière-plan (injectée dans <body>), carte centrée au premier plan."""
    ss = st.session_state
    # Feuille de style + en-tête de la carte dans UN seul bloc (pas d'espace parasite dans la carte)
    st.markdown(LOGIN_CSS + f'<div class="login-head">{LOGO}<h1>{APP_NAME}</h1><p>{TAGLINE}</p></div>',
                unsafe_allow_html=True)
    flash = ss.pop("auth_msg", None)
    if flash:
        getattr(st, flash[0])(flash[1])
    t1, t2 = st.tabs(["Se connecter", "Créer un compte"])
    with t1:
        bloque = ss["echecs"] >= MAX_ECHECS
        with st.form("form_connexion"):
            st.text_input("E-mail", key="l_user", autocomplete="username")
            st.text_input("Mot de passe", type="password", key="l_pwd", autocomplete="current-password")
            st.form_submit_button("Se connecter", type="primary", on_click=cb_connexion, disabled=bloque,
                                  use_container_width=True)
        if bloque:
            st.error("Trop de tentatives échouées. Rechargez la page pour réessayer.")
        elif ss["echecs"] > 0:
            st.error(f"E-mail ou mot de passe incorrect ({ss['echecs']}/{MAX_ECHECS}).")
    with t2:
        with st.form("form_inscription"):
            c1, c2 = st.columns(2)
            c1.text_input("Prénom", key="i_prenom", autocomplete="given-name")
            c2.text_input("Nom", key="i_nom", autocomplete="family-name")
            st.text_input("E-mail", key="i_email", autocomplete="email")
            st.text_input("Mot de passe (8 caractères minimum)", type="password", key="i_pwd", autocomplete="new-password")
            st.text_input("Confirmer le mot de passe", type="password", key="i_pwd2", autocomplete="new-password")
            st.form_submit_button("Créer mon compte", type="primary", on_click=cb_inscription,
                                  use_container_width=True)
    # Vidéo, voile et slogan : injectés dans le <body> du document parent, HORS de .block-container
    try:
        components.html(LOGIN_BG_JS, height=0)
    except Exception:
        pass        # sans le script : fond bleu nuit uni, la carte reste utilisable

# === 3 lignes à ajouter par ailleurs ===
# a) début de application() :  components.html(NETTOYER_FOND_JS, height=0)
# b) dans le CSS du dashboard, après '#MainMenu,footer{visibility:hidden}' :
#    [data-testid="stElementContainer"]:has(> iframe[height="0"]){position:absolute;width:0;height:0;overflow:hidden;margin:0}
