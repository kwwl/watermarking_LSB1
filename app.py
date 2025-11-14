import streamlit as st
from PIL import Image
import io


def text_to_binaire(texte):
    return "".join(format(ord(c), "08b") for c in texte)


def pixels_pairs(image):
    pixels = list(image.getdata())
    pixels_pairs = [p if p % 2 == 0 else p - 1 for p in pixels]
    new_img = Image.new("L", image.size)
    new_img.putdata(pixels_pairs)
    return new_img


def encoder_message(image, message):
    message_binaire = text_to_binaire(message) + "1111111111111110"
    pixels = list(image.getdata())

    if len(message_binaire) > len(pixels):
        raise ValueError("Le message est trop long par rapport au nombre de pixels")

    pixels_modifies = []
    for i in range(len(message_binaire)):
        pixel = pixels[i]
        if message_binaire[i] == "1":
            pixels_modifies.append(pixel + 1)
        else:
            pixels_modifies.append(pixel)

    pixels_modifies += pixels[len(message_binaire) :]

    new_img = Image.new("L", image.size)
    new_img.putdata(pixels_modifies)
    return new_img


def decoder_message(image):
    pixels = list(image.getdata())
    bits = [str(p % 2) for p in pixels]
    message_binaire = "".join(bits)

    octets = [message_binaire[i : i + 8] for i in range(0, len(message_binaire), 8)]

    message = ""
    for octet in octets:
        if octet == "11111111":
            break
        message += chr(int(octet, 2))

    return message


st.set_page_config(page_title="Image Steganography", page_icon="🔒", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #1e293b;
        color: white;
        border-radius: 10px;
        padding: 0.75rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #334155;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .upload-box {
        border: 2px dashed #cbd5e1;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: white;
        transition: all 0.3s;
    }
    .success-box {
        background: #dcfce7;
        border: 2px solid #86efac;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #fef3c7;
        border: 2px solid #fcd34d;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    h1 {
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🔒 Image Steganography")
st.markdown(
    '<p class="subtitle">Cachez des messages secrets dans vos images en utilisant la technique LSB</p>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    ["📝 Encoder un message", "🔓 Décoder un message", "ℹ️ À propos"]
)

with tab1:
    st.markdown("### 🔐 Encoder un message secret")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 📤 Charger une image")
        uploaded_file = st.file_uploader(
            "Choisissez une image",
            type=["png", "jpg", "jpeg"],
            key="encode_upload",
            help="Formats supportés: PNG, JPG, JPEG",
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("L")
            st.image(image, caption="Image originale", use_container_width=True)

            st.markdown("#### ✍️ Message secret")
            message = st.text_area(
                "Entrez votre message",
                placeholder="Tapez votre message secret ici...",
                height=150,
                help="Le message sera caché dans les pixels de l'image",
            )

            if st.button("🔒 Encoder le message", type="primary"):
                if message:
                    try:
                        with st.spinner("Encodage en cours..."):
                            img_pairs = pixels_pairs(image)
                            img_encoded = encoder_message(img_pairs, message)

                            st.session_state["encoded_image"] = img_encoded
                            st.session_state["message_encoded"] = True

                        st.success("✅ Message encodé avec succès!")
                        st.balloons()
                    except ValueError as e:
                        st.error(f"❌ Erreur: {str(e)}")
                else:
                    st.warning("⚠️ Veuillez entrer un message à encoder")

    with col2:
        st.markdown("#### 🖼️ Résultat")

        if "encoded_image" in st.session_state and st.session_state.get(
            "message_encoded"
        ):
            encoded_img = st.session_state["encoded_image"]

            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("**✨ Image encodée avec succès!**")
            st.markdown("Le message est maintenant invisible à l'œil nu")
            st.markdown("</div>", unsafe_allow_html=True)

            st.image(
                encoded_img,
                caption="Image avec message caché",
                use_container_width=True,
            )

            buf = io.BytesIO()
            encoded_img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Télécharger l'image encodée",
                data=byte_im,
                file_name="image_encoded.png",
                mime="image/png",
                use_container_width=True,
            )

            st.info(
                "💡 **Astuce:** Téléchargez cette image et utilisez l'onglet 'Décoder' pour retrouver le message caché"
            )
        else:
            st.markdown('<div class="upload-box">', unsafe_allow_html=True)
            st.markdown("📸")
            st.markdown("**L'image encodée apparaîtra ici**")
            st.markdown("Chargez une image et entrez un message pour commencer")
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔓 Décoder un message caché")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 📤 Charger l'image encodée")
        decode_file = st.file_uploader(
            "Choisissez une image encodée",
            type=["png", "jpg", "jpeg"],
            key="decode_upload",
            help="Chargez une image contenant un message caché",
        )

        if decode_file is not None:
            decode_image = Image.open(decode_file).convert("L")
            st.image(decode_image, caption="Image encodée", use_container_width=True)

            if st.button("🔓 Décoder le message", type="primary"):
                try:
                    with st.spinner("Décodage en cours..."):
                        decoded_msg = decoder_message(decode_image)
                        st.session_state["decoded_message"] = decoded_msg

                    st.success("✅ Message décodé avec succès!")
                except Exception as e:
                    st.error(f"❌ Erreur lors du décodage: {str(e)}")

    with col2:
        st.markdown("#### 📨 Message décodé")

        if "decoded_message" in st.session_state:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("**🔓 Message secret révélé:**")
            st.markdown("</div>", unsafe_allow_html=True)

            st.text_area(
                "",
                value=st.session_state["decoded_message"],
                height=200,
                disabled=True,
                key="decoded_text",
            )

            if st.button("📋 Copier le message"):
                st.code(st.session_state["decoded_message"], language=None)
        else:
            st.markdown('<div class="upload-box">', unsafe_allow_html=True)
            st.markdown("💬")
            st.markdown("**Le message décodé apparaîtra ici**")
            st.markdown("Chargez une image encodée pour révéler le message secret")
            st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### ℹ️ À propos de la stéganographie")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div style="background: white; padding: 1.5rem; border-radius: 15px; height: 100%;">
            <h4>🔐 Sécurité invisible</h4>
            <p>Les messages sont cachés dans les données des pixels, les rendant complètement invisibles sans décodage.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div style="background: white; padding: 1.5rem; border-radius: 15px; height: 100%;">
            <h4>🖼️ Qualité d'image</h4>
            <p>L'image encodée semble identique à l'originale, préservant la qualité visuelle complète.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div style="background: white; padding: 1.5rem; border-radius: 15px; height: 100%;">
            <h4>🔓 Récupération facile</h4>
            <p>Toute personne avec l'image encodée peut extraire le message caché en utilisant le décodeur.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### 🔬 Comment ça marche?")

    st.markdown(
        """
    La **stéganographie LSB (Least Significant Bit)** est une technique qui cache des informations dans les bits les moins significatifs des pixels d'une image.

    #### 📝 Processus d'encodage:
    1. **Conversion du texte** → Le message est converti en binaire (0 et 1)
    2. **Normalisation des pixels** → Les pixels sont rendus pairs pour préparer l'encodage
    3. **Modification des LSB** → Les bits du message remplacent les bits les moins significatifs des pixels
    4. **Marqueur de fin** → Un marqueur spécial indique la fin du message

    #### 🔍 Processus de décodage:
    1. **Extraction des LSB** → Les bits les moins significatifs sont extraits de chaque pixel
    2. **Reconstruction** → Les bits sont regroupés en octets (8 bits)
    3. **Conversion** → Les octets sont convertis en caractères
    4. **Arrêt** → La lecture s'arrête au marqueur de fin

    #### ✨ Avantages:
    - ✅ Invisible à l'œil nu
    - ✅ Aucune perte de qualité perceptible
    - ✅ Simple et efficace
    - ✅ Difficile à détecter sans analyse approfondie
    """
    )

    st.markdown("---")

    st.markdown(
        """
    <div style="text-align: center; color: #64748b; padding: 2rem;">
        <p>Développé avec ❤️ en utilisant Python, Streamlit et PIL</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

if "encoded_image" not in st.session_state:
    st.session_state["encoded_image"] = None
if "message_encoded" not in st.session_state:
    st.session_state["message_encoded"] = False
if "decoded_message" not in st.session_state:
    st.session_state["decoded_message"] = None
