import streamlit as st
from PIL import Image
import io
from main import encoder_message, decoder_message

st.set_page_config(page_title="LSB1 Watermarking", layout="wide")

st.title("🔐 LSB1 - Stéganographie avec mot de passe")

tab1, tab2 = st.tabs(["Encoder", "Decoder"])

with tab1:
    st.header("Encoder un message")

    uploaded_img = st.file_uploader("Choisir une image", type=["png", "jpg", "jpeg"])
    password = st.text_input("Mot de passe à cacher", type="password")

    if uploaded_img:
        image = Image.open(uploaded_img).convert("L")
        st.image(image, caption="Image d'origine", use_container_width=True)

    if uploaded_img and password:
        if st.button("Encoder dans l'image"):
            encoded_img = encoder_message(image, password)

            # Convertir en bytes téléchargeables
            img_bytes = io.BytesIO()
            encoded_img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            st.success("Mot de passe encodé avec succès !")
            st.image(encoded_img, caption="Image encodée", use_container_width=True)

            st.download_button(
                "Télécharger l'image encodée",
                img_bytes,
                file_name="encoded.png",
                mime="image/png",
            )


with tab2:
    st.header("Décoder un message")

    uploaded_img2 = st.file_uploader(
        "Image à décoder", type=["png", "jpg", "jpeg"], key="decode"
    )

    if uploaded_img2:
        image2 = Image.open(uploaded_img2).convert("L")
        st.image(image2, caption="Image chargée", use_container_width=True)

        if st.button("Décoder le message"):
            try:
                message = decoder_message(image2)
                st.success("Message trouvé :")
                st.code(message)
            except:
                st.error("Impossible de décoder un message dans cette image.")
