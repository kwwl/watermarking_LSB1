# 🔐 LSB1 Watermarking
Stéganographie d’un mot de passe dans une image — Projet réalisé dans le cadre d’un TP universitaire
🌍 Démo en ligne

👉 https://watermarkinglsb1.streamlit.app/

(Aucune installation nécessaire — interface Streamlit)

## 📝 Présentation du projet

Ce projet a été réalisé dans le cadre d’un Travaux Pratique (TP) de cours, visant à introduire les concepts de :

Stéganographie

Manipulation des bits (LSB1)

Traitement d’images

Interface utilisateur en Python

Séparation propre backend / frontend

Déploiement sur Streamlit Cloud

Le but : cacher un mot de passe dans une image en modifiant les bits les moins significatifs des pixels, sans altérer visuellement l’image.

✨ Fonctionnalités principales
## 🔐 Encodage

Upload d’une image (PNG/JPG)

Conversion en niveaux de gris

Mise à zéro des pixels impairs (normalisation)

Encodage bit par bit du message

Ajout d’un marqueur de fin "1111111111111110"

Affichage de l'image encodée

Téléchargement direct

## 🔓 Décodage

Extraction automatique des LSB

Reconstruction du message original

Affichage en clair dans l’interface

## 🧠 Architecture claire

main.py → toutes les fonctions de traitement (backend)

app.py → interface Streamlit (frontend)

## 🏗️ Structure du projet
📁 LSB1-Watermarking
│
├── app.py                # Interface Streamlit (frontend)
├── main.py               # Algorithmes de stéganographie (backend)
├── requirements.txt      # Dépendances Python
└── asset/                # Images utilisées pour les tests

## ⚙️ Installation & Lancement
1️⃣ Cloner le repository
git clone https://github.com/USERNAME/LSB1-watermarking.git
cd LSB1-watermarking

2️⃣ Installer les dépendances
pip install -r requirements.txt

3️⃣ Lancer l'application
streamlit run app.py

## 🔬 Comment fonctionne la méthode LSB1 ?

La stéganographie LSB1 (Least Significant Bit 1) consiste à modifier uniquement le bit le moins significatif de chaque pixel.

## ✔️ Étapes d'encodage

Transformer le message en binaire

S’assurer que tous les pixels sont pairs

Injecter les bits du message dans les LSB

Ajouter un marqueur final pour stopper la lecture

## ✔️ Étapes de décodage

Récupérer tous les LSB des pixels

Regrouper les bits par blocs de 8

Convertir chaque bloc en caractère

Arrêter au marqueur de fin

🎯 Invisible à l’œil, parfaitement réversible.

🛠️ Technologies utilisées

Python 3

Streamlit (UI)

Pillow (PIL) (traitement d’image)

GitHub + Streamlit Cloud (déploiement)

## 🧑‍🏫 Contexte académique

Ce projet a été conçu pour :

comprendre les méthodes d’encodage de messages,

apprendre la manipulation à bas niveau des bits,

développer une interface ergonomique,

travailler comme dans un vrai environnement logiciel.

Il s’agit d’un TP pédagogique, pas d’un outil de cybersécurité avancé.

## ⭐ Améliorations possibles

Support des images en couleur (3 canaux)

Cryptage du message avant encodage

Interface en mode clair/sombre

Détection automatique de corruption de message
