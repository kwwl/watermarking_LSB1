import streamlit as st
from PIL import Image
from io import BytesIO
import hashlib

# Essayer d'importer Fernet pour chiffrement symétrique (optionnel)
try:
    from cryptography.fernet import Fernet

    HAS_FERNET = True
except Exception:
    HAS_FERNET = False


# ---------------------------
# Fonctions LSB1 (niveaux de gris)
# ---------------------------
def texte_en_binaire(texte: str) -> str:
    """Convertit le texte en chaîne binaire (8 bits par caractère)."""
    return "".join(format(ord(c), "08b") for c in texte)


END_MARKER = "1111111111111110"  # marqueur de fin


def pixels_pairs(image: Image.Image) -> Image.Image:
    """Rend tous les pixels pair (LSB = 0). On travaille en niveaux de gris."""
    pixels = list(image.getdata())
    pixels_pairs = [p if p % 2 == 0 else p - 1 for p in pixels]
    new_img = Image.new("L", image.size)
    new_img.putdata(pixels_pairs)
    return new_img


def encoder_message(image: Image.Image, message: str) -> Image.Image:
    """
    Encode message (str) dans l'image (mode 'L') en modifiant le LSB de chaque pixel.
    Retourne une nouvelle Image.
    """
    if image.mode != "L":
        raise ValueError("L'image doit être en niveaux de gris (mode 'L').")

    message_binaire = texte_en_binaire(message) + END_MARKER
    pixels = list(image.getdata())

    if len(message_binaire) > len(pixels):
        raise ValueError("Le message est trop long pour cette image (trop de bits).")

    pixels_modifies = []
    for i in range(len(message_binaire)):
        pixel = pixels[i]
        # on suppose que les pixels de base sont pairs (si ce n'est pas le cas,
        # appeler pixels_pairs avant)
        if message_binaire[i] == "1":
            # si pixel est 255 (max) et impair on ne veut pas dépasser, on gère marge
            if pixel == 255:
                pixels_modifies.append(
                    254
                )  # 254 est pair -> LSB=0 mais force variation minimale
            else:
                pixels_modifies.append(pixel + 1)
        else:
            # si pixel est impair, on le rend pair ; si déjà pair on laisse
            if pixel % 2 == 0:
                pixels_modifies.append(pixel)
            else:
                pixels_modifies.append(pixel - 1)

    # ajouter le reste non modifié
    pixels_modifies += pixels[len(message_binaire) :]

    new_img = Image.new("L", image.size)
    new_img.putdata(pixels_modifies)
    return new_img


def decoder_message(image: Image.Image) -> str:
    """Lit les LSB de l'image et reconstruit le message jusqu'au marqueur de fin."""
    pixels = list(image.getdata())
    bits = "".join(str(p % 2) for p in pixels)
    # Chercher marqueur de fin
    end_idx = bits.find(END_MARKER)
    if end_idx == -1:
        # pas de marqueur trouvé
        return ""

    useful_bits = bits[:end_idx]  # tout jusqu'au marqueur (exclu)
    # reconstruire par octets
    octets = [useful_bits[i : i + 8] for i in range(0, len(useful_bits), 8)]
    message_chars = []
    for o in octets:
        if len(o) < 8:
            break
        try:
            message_chars.append(chr(int(o, 2)))
        except Exception:
            message_chars.append("?")
    return "".join(message_chars)


# ---------------------------
# Utilitaires
# ---------------------------
def image_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    bio = BytesIO()
    img.save(bio, format=fmt)
    return bio.getvalue()


def generate_fernet_key() -> bytes:
    return Fernet.generate_key()


def fernet_encrypt(key: bytes, plaintext: str) -> bytes:
    f = Fernet(key)
    return f.encrypt(plaintext.encode())


def fernet_decrypt(key: bytes, ciphertext: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()


# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="LSB1 Watermarking (Pillow) - Démo", layout="wide")

st.title("Démo LSB1 — cacher un mot de passe dans une image (Pillow + Streamlit)")
st.markdown(
    """
Cette application illustre l'algorithme **LSB1** (Least Significant Bit).
- L'image est convertie en niveaux de gris (mode 'L').
- Chaque pixel stocke 1 bit du message dans son LSB.
- Un marqueur de fin est ajouté pour retrouver la longueur du message.
"""
)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1) Charger une image")
    uploaded = st.file_uploader(
        "Choisis une image (jpg/png). Elle sera convertie en niveaux de gris.",
        type=["png", "jpg", "jpeg"],
    )
    if uploaded is not None:
        img = Image.open(uploaded).convert("L")
        st.image(
            img,
            caption="Image convertie en niveaux de gris (originale)",
            use_column_width=True,
        )
    else:
        st.info("Upload une image pour commencer.")

with col2:
    st.header("2) Entrer le mot de passe à cacher")
    mdp = st.text_input("Mot de passe (mdp) à cacher", type="password")
    show_binary = st.checkbox("Afficher le binaire du mot de passe", value=False)
    show_pixels_prep = st.checkbox(
        "Forcer pixels pairs avant encodage (recommandé)", value=True
    )

st.markdown("---")

# Affichage du binaire du mdp
if mdp and show_binary:
    st.subheader("Binaire du mot de passe")
    b = texte_en_binaire(mdp)
    st.code(b)

# Encodage + affichage
st.header("Encodage / Décodage")
colA, colB, colC = st.columns([1, 1, 1])

with colA:
    if uploaded is None:
        st.write("Upload une image pour encoder.")
    else:
        if st.button("Encoder le mdp dans l'image"):
            try:
                base_img = img.copy()
                if show_pixels_prep:
                    base_img = pixels_pairs(base_img)
                encoded = encoder_message(base_img, mdp)
                st.success("Encodage terminé ✅")
                # stocker dans le state temporaire
                st.session_state["encoded_image_bytes"] = image_to_bytes(
                    encoded, fmt="PNG"
                )
                st.session_state["encoded_image_obj"] = encoded
            except Exception as e:
                st.error(f"Erreur pendant l'encodage : {e}")

with colB:
    if "encoded_image_obj" in st.session_state:
        st.image(
            st.session_state["encoded_image_obj"],
            caption="Image encodée",
            use_column_width=True,
        )
        st.download_button(
            "Télécharger l'image encodée (PNG)",
            data=st.session_state["encoded_image_bytes"],
            file_name="encoded.png",
            mime="image/png",
        )
    else:
        st.info("Après encodage, l'image encodée apparaîtra ici.")

with colC:
    if "encoded_image_obj" in st.session_state:
        if st.button("Décoder le message depuis l'image encodée"):
            decoded = decoder_message(st.session_state["encoded_image_obj"])
            if decoded:
                st.success("Message décodé :")
                st.write(decoded)
            else:
                st.warning("Aucun message détecté (marqueur de fin introuvable).")
    else:
        st.info("Encode d'abord pour ensuite décoder.")

st.markdown("---")

# Section chiffrement / hash du mdp
st.header("Chiffrement / Hash du mot de passe (affichage)")

colE, colF = st.columns(2)
with colE:
    st.subheader("SHA-256 (hash)")
    if mdp:
        sha = hashlib.sha256(mdp.encode()).hexdigest()
        st.code(sha)
    else:
        st.write("Renseigne un mot de passe pour afficher son hash SHA-256.")

with colF:
    st.subheader("Chiffrement symétrique (Fernet) — optionnel")
    if not HAS_FERNET:
        st.info(
            "La librairie 'cryptography' n'est pas installée. Installe-la pour tester Fernet."
        )
    else:
        key = st.session_state.get("fernet_key", None)
        if key is None:
            if st.button("Générer une clé Fernet"):
                new_key = generate_fernet_key()
                st.session_state["fernet_key"] = new_key
                st.success("Clé générée et stockée en session.")
                key = new_key
        if key:
            st.code(key.decode())
            if mdp:
                if st.button("Chiffrer le mot de passe (Fernet)"):
                    ct = fernet_encrypt(key, mdp)
                    st.session_state["fernet_ct"] = ct
                    st.success("Mot de passe chiffré (Fernet).")
                if "fernet_ct" in st.session_state:
                    st.subheader("Texte chiffré (base64)")
                    st.code(st.session_state["fernet_ct"].decode())

st.markdown("---")
st.caption(
    "Remarque : l'interface montre des démonstrations pédagogiques. En production, ne jamais afficher ni stocker des mots de passe en clair."
)

# Footer : afficher image originale et encodée côte-à-côte si dispo
st.header("Aperçu final")
if uploaded:
    if "encoded_image_obj" in st.session_state:
        c1, c2 = st.columns(2)
        with c1:
            st.image(img, caption="Original (gris)", use_column_width=True)
        with c2:
            st.image(
                st.session_state["encoded_image_obj"],
                caption="Encodée",
                use_column_width=True,
            )
    else:
        st.image(img, caption="Original (gris)", use_column_width=True)
