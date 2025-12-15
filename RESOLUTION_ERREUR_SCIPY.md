# ❌ Erreur: "No matching distribution found for scipy>=1.16.3"

## 🐛 Problème

Vous obtenez cette erreur lors de l'installation :
```
ERROR: No matching distribution found for scipy>=1.16.3
```

---

## ✅ Solution rapide (2 minutes)

**N'utilisez PAS `requirements_app.txt`**. À la place :

```bash
# 1. Installer FaceFusion (inclut tout)
cd facefusion
python install.py
cd ..

# 2. Installer uniquement Gradio
pip install gradio gradio-rangeslider

# 3. Lancer l'application
python actor_faceswap_studio.py
```

**C'est tout !** 🎉

---

## 📖 Explication

### Pourquoi cette erreur ?

Le fichier `requirements_app.txt` listait des versions futures de bibliothèques qui n'existent pas encore (comme scipy 1.16.3).

### Pourquoi cette solution fonctionne ?

L'outil `install.py` de FaceFusion :
- ✅ Détecte automatiquement les bonnes versions
- ✅ Gère les dépendances correctement
- ✅ S'adapte à votre système (macOS/Linux/Windows)
- ✅ Télécharge les modèles nécessaires

Ensuite vous ajoutez juste Gradio (l'interface web), qui est la seule dépendance supplémentaire pour votre application.

---

## 🔧 Méthode alternative complète

Si vous voulez tout contrôler manuellement :

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# 2. Mettre à jour pip
pip install --upgrade pip

# 3. Installer les dépendances avec versions stables
pip install gradio>=4.44.0
pip install gradio-rangeslider
pip install "numpy>=1.24.0,<2.0.0"
pip install "scipy>=1.11.0,<1.15.0"
pip install opencv-python>=4.8.0
pip install onnxruntime>=1.16.0
pip install onnx>=1.15.0
pip install tqdm>=4.65.0
pip install psutil>=5.9.0
pip install pillow>=10.0.0
pip install requests>=2.31.0

# 4. Lancer l'application
python actor_faceswap_studio.py
```

---

## 🎯 Commandes pour chaque situation

### Situation 1: Vous n'avez rien installé encore

```bash
cd facefusion
python install.py
cd ..
pip install gradio gradio-rangeslider
python actor_faceswap_studio.py
```

### Situation 2: Vous avez déjà essayé `pip install -r requirements_app.txt`

```bash
# Réinstallez FaceFusion pour corriger les versions
cd facefusion
pip install -r requirements.txt --force-reinstall
cd ..
pip install gradio gradio-rangeslider
python actor_faceswap_studio.py
```

### Situation 3: Vous voulez repartir de zéro

```bash
# 1. Supprimer l'environnement actuel
deactivate  # si vous êtes dans un venv

# 2. Créer un nouvel environnement
python -m venv venv_facefusion
source venv_facefusion/bin/activate  # macOS/Linux
# ou
venv_facefusion\Scripts\activate     # Windows

# 3. Installer
cd facefusion
python install.py
cd ..
pip install gradio gradio-rangeslider

# 4. Lancer
python actor_faceswap_studio.py
```

---

## ✅ Vérifier que tout fonctionne

Testez votre installation :

```bash
python -c "
import gradio as gr
import sys
sys.path.insert(0, 'facefusion')
from facefusion import state_manager
print('✅ Installation réussie !')
print(f'Gradio version: {gr.__version__}')
"
```

Si ça affiche "✅ Installation réussie !", vous êtes prêt !

---

## 🆘 Toujours des erreurs ?

### Erreur: "ModuleNotFoundError: No module named 'gradio'"
```bash
pip install gradio gradio-rangeslider
```

### Erreur: "No module named 'facefusion'"
```bash
# Vérifiez que vous êtes dans le bon dossier
ls facefusion/facefusion.py  # doit exister

# Installez FaceFusion
cd facefusion
python install.py
cd ..
```

### Erreur: Python version
```bash
python --version  # Doit être 3.10 ou 3.11

# Si trop vieux, installez Python 3.11
# macOS: brew install python@3.11
# Windows: python.org
```

---

## 📚 Documentation complète

Pour plus d'informations, consultez :
- [INSTALLATION_ALTERNATIVE.md](INSTALLATION_ALTERNATIVE.md) - Méthodes d'installation détaillées
- [README_APP.md](README_APP.md#-dépannage) - Section dépannage complète
- [START_HERE.md](START_HERE.md) - Guide de démarrage

---

## 💡 Résumé

**La solution la plus simple** :

```bash
cd facefusion && python install.py && cd ..
pip install gradio gradio-rangeslider
python actor_faceswap_studio.py
```

**Ouvrez votre navigateur à** : http://localhost:7860

**Et voilà !** 🎉
