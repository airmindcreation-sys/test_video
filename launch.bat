@echo off
REM 🎬 Actor Face Swap Studio - Script de lancement
REM Pour Windows

echo ==================================
echo 🎬 Actor Face Swap Studio
echo ==================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo 📥 Installez Python 3.10+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Vérifier si FaceFusion existe
if not exist "facefusion" (
    echo ❌ Le dossier 'facefusion' n'existe pas
    echo 📥 Clonez d'abord le dépôt FaceFusion:
    echo    git clone https://github.com/facefusion/facefusion.git
    pause
    exit /b 1
)

echo ✅ FaceFusion trouvé

REM Vérifier si les dépendances sont installées
python -c "import gradio" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Installation des dépendances...
    pip install -r requirements_app.txt
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
)

echo ✅ Dépendances installées
echo.
echo 🚀 Lancement de l'application...
echo 🌐 L'interface s'ouvrira automatiquement dans votre navigateur
echo 📍 Adresse: http://localhost:7860
echo.
echo 💡 Astuce: Appuyez sur Ctrl+C pour arrêter l'application
echo.
echo ==================================
echo.

REM Lancer l'application
python actor_faceswap_studio.py

pause
