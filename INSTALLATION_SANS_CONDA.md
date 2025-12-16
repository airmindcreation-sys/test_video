# 🚀 Installation SANS Conda (Version simplifiée)

FaceFusion recommande Conda, mais voici comment l'installer **sans Conda** pour utiliser votre application.

## ⚡ Installation rapide (Mac/Linux)

### 1. Prérequis système

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg git curl
```

### 2. Installation Python (sans conda)

```bash
cd "/Users/martinemenguy/Desktop/for facefusion"

# Créer un environnement virtuel Python
python3 -m venv venv_facefusion

# Activer l'environnement
source venv_facefusion/bin/activate  # macOS/Linux
# ou
venv_facefusion\Scripts\activate     # Windows
```

### 3. Installer FaceFusion

```bash
cd facefusion

# Installer avec le script officiel
python install.py --onnxruntime default

# Revenir au dossier parent
cd ..
```

### 4. Installer Gradio

```bash
pip install gradio gradio-rangeslider
```

### 5. Lancer l'application

```bash
python actor_faceswap_studio.py
```

---

## 🐧 Pour serveur RunPod/Linux avec GPU

### Installation complète

```bash
# 1. Système
apt update
apt install -y ffmpeg git curl python3-pip

# 2. Votre application
cd /workspace
git clone <votre-repo> facefusion-app
cd facefusion-app

# 3. FaceFusion
cd facefusion
python3 install.py --onnxruntime cuda  # CUDA pour GPU
cd ..

# 4. Gradio
pip3 install gradio gradio-rangeslider

# 5. GPU support
pip3 uninstall onnxruntime -y
pip3 install onnxruntime-gpu

# 6. Vérifier CUDA
python3 -c "import onnxruntime as ort; print(ort.get_available_providers())"
# Doit afficher: ['CUDAExecutionProvider', ...]

# 7. Lancer
python3 actor_faceswap_studio.py
```

---

## 🔧 Alternative : Utiliser FaceFusion directement

Si l'intégration est trop complexe, vous pouvez aussi utiliser FaceFusion en ligne de commande :

```bash
cd facefusion

# Face swap simple
python facefusion.py headless-run \
  --source-paths photo_acteur.jpg \
  --target-path video.mp4 \
  --output-path result.mp4 \
  --processors face_swapper \
  --face-swapper-model inswapper_128

# Avec lip sync
python facefusion.py headless-run \
  --source-paths photo_acteur.jpg \
  --target-path video.mp4 \
  --output-path result.mp4 \
  --processors face_swapper lip_syncer \
  --face-swapper-model inswapper_128 \
  --lip-syncer-model wav2lip_gan
```

Puis intégrez juste l'UI Gradio qui appelle cette commande !

---

## 💡 Recommendation

**Pour votre cas d'usage**, je recommande de :

1. **Utiliser FaceFusion CLI** en headless mode
2. **Créer une interface Gradio** qui génère les bonnes commandes
3. **Lancer les commandes** via subprocess

C'est plus simple et plus stable que d'essayer d'importer les modules internes de FaceFusion.

Voulez-vous que je crée cette version simplifiée ?
