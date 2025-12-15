#!/bin/bash

# 🎬 Actor Face Swap Studio - Script de lancement
# Pour macOS et Linux

echo "=================================="
echo "🎬 Actor Face Swap Studio"
echo "=================================="
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "📥 Installez Python 3.10+ depuis https://www.python.org/"
    exit 1
fi

# Vérifier la version de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION détecté, mais Python 3.10+ est requis"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION détecté"

# Vérifier que ffmpeg est installé
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg n'est pas installé"
    echo "📥 Installation recommandée:"
    echo "   macOS: brew install ffmpeg"
    echo "   Linux: sudo apt install ffmpeg"
    echo ""
    read -p "Voulez-vous continuer sans ffmpeg ? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ ffmpeg détecté"
fi

# Vérifier si FaceFusion est installé
if [ ! -d "facefusion" ]; then
    echo "❌ Le dossier 'facefusion' n'existe pas"
    echo "📥 Clonez d'abord le dépôt FaceFusion:"
    echo "   git clone https://github.com/facefusion/facefusion.git"
    exit 1
fi

echo "✅ FaceFusion trouvé"

# Vérifier si les dépendances sont installées
if ! python3 -c "import gradio" &> /dev/null; then
    echo ""
    echo "📦 Installation des dépendances..."
    pip3 install -r requirements_app.txt

    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'installation des dépendances"
        exit 1
    fi
fi

echo "✅ Dépendances installées"
echo ""
echo "🚀 Lancement de l'application..."
echo "🌐 L'interface s'ouvrira automatiquement dans votre navigateur"
echo "📍 Adresse: http://localhost:7860"
echo ""
echo "💡 Astuce: Appuyez sur Ctrl+C pour arrêter l'application"
echo ""
echo "=================================="
echo ""

# Lancer l'application
python3 actor_faceswap_studio.py
