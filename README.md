🔐 LSB1 Watermarking – Stéganographie & Encodage de Mot de Passe

📘 Projet réalisé dans le cadre d’un TP de cours portant sur la stéganographie et l’exploitation du LSB1.

Une application moderne permettant de cacher un mot de passe dans une image grâce à la stéganographie LSB1 (Least Significant Bit).
Développée en Python avec Streamlit pour l’interface et Pillow pour le traitement d’images.

🌍 💻 Version en ligne (déployée)

Accédez à l'application ici :
👉 https://watermarkinglsb1.streamlit.app/

Aucune installation nécessaire.
Upload une image → encode → télécharge → décode.

🎓 Contexte pédagogique

Ce projet a été développé dans le cadre d’un Travaux Pratique (TP) visant à :

comprendre la stéganographie par manipulation des bits les moins significatifs (LSB),

concevoir une séparation claire backend / frontend,

produire une interface moderne,

expérimenter un workflow complet : codage → interface → déploiement.

Il ne s’agit pas d’un outil de sécurité avancé mais d’une démonstration académique.

🌟 Fonctionnalités
✔️ Encodage d’un mot de passe

Upload image PNG/JPG

Conversion en niveaux de gris

Encodage dans les LSB

Marqueur de fin sécurisé

Visualisation avant / après

Téléchargement de l’image encodée

✔️ Décodage

Extraction automatique du message caché

Affichage instantané du mot de passe

✔️ Séparation logique du code

main.py → backend (fonctions)

app.py → frontend (Streamlit UI)

🚀 Installation
1️⃣ Cloner le repo
git clone https://github.com/USERNAME/LSB1-watermarking.git
cd LSB1-watermarking

2️⃣ Installer les dépendances
pip install -r requirements.txt

3️⃣ Lancer l’app
streamlit run app.py

🔎 Fonctionnement LSB1 en bref

Le dernier bit (LSB) d’un pixel peut être modifié sans impact visuel.
Ton message converti en binaire vient remplacer ces bits un par un.

✔️ Invisible
✔️ Réversible
✔️ Parfait pour un TP pédagogique

📂 Structure
📁 LSB1-watermarking
 ├── app.py
 ├── main.py
 ├── requirements.txt
 └── asset/

🛠️ Technologies

Python

Streamlit

Pillow (PIL)

Stéganographie LSB1
