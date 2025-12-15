# 🔧 Installation Alternative (Recommandée)

Si vous rencontrez des erreurs avec `requirements_app.txt`, suivez cette méthode alternative qui utilise directement les dépendances de FaceFusion.

---

## ✅ Méthode recommandée (3 étapes)

### Étape 1: Installer FaceFusion complet

```bash
cd facefusion
python install.py
```

Cette commande installe **toutes** les dépendances nécessaires, y compris celles pour votre application.

### Étape 2: Installer uniquement Gradio (pour l'interface)

```bash
cd ..
pip install gradio gradio-rangeslider
```

### Étape 3: Lancer l'application

```bash
./launch.sh          # macOS/Linux
# ou
launch.bat           # Windows
```

---

## 🎯 Pourquoi cette méthode ?

Le fichier `install.py` de FaceFusion :
- ✅ Gère automatiquement les versions compatibles
- ✅ Télécharge les modèles nécessaires
- ✅ Vérifie les prérequis système
- ✅ Installe les bonnes versions selon votre OS

Ensuite, vous ajoutez juste Gradio pour l'interface personnalisée.

---

## 🐛 Si vous avez des erreurs de version

### Erreur: "No matching distribution found for scipy>=1.16.3"

**Cause**: Les versions dans requirements.txt sont trop récentes

**Solution**:
```bash
cd facefusion
pip install -r requirements.txt
cd ..
pip install gradio gradio-rangeslider
```

### Erreur: "Conflict with numpy 2.x"

**Solution**: Utilisez numpy 1.x
```bash
pip install "numpy>=1.24.0,<2.0.0"
pip install gradio gradio-rangeslider
```

### Erreur générale de dépendances

**Solution complète**:
```bash
# 1. Créer un environnement virtuel propre
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# 2. Installer FaceFusion
cd facefusion
pip install -r requirements.txt
cd ..

# 3. Installer Gradio
pip install gradio>=4.44.0 gradio-rangeslider

# 4. Lancer l'app
python actor_faceswap_studio.py
```

---

## 📦 Installation manuelle des dépendances principales

Si vous préférez installer manuellement avec des versions stables :

```bash
# Interface
pip install gradio>=4.44.0
pip install gradio-rangeslider

# Core (versions stables testées)
pip install numpy>=1.24.0,<2.0.0
pip install scipy>=1.11.0,<1.15.0
pip install opencv-python>=4.8.0
pip install onnxruntime>=1.16.0
pip install onnx>=1.15.0
pip install tqdm>=4.65.0
pip install psutil>=5.9.0
pip install pillow>=10.0.0
pip install requests>=2.31.0
```

---

## 🚀 Support GPU (NVIDIA)

Si vous avez une carte graphique NVIDIA avec CUDA :

```bash
# 1. Désinstaller onnxruntime CPU
pip uninstall onnxruntime

# 2. Installer onnxruntime-gpu
pip install onnxruntime-gpu>=1.16.0

# 3. Vérifier CUDA
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
# Devrait afficher: ['CUDAExecutionProvider', 'CPUExecutionProvider']
```

---

## ✅ Vérification de l'installation

Testez que tout est installé correctement :

```bash
python -c "
import gradio
import numpy
import cv2
import onnxruntime
print('✅ Toutes les dépendances sont installées !')
print(f'Gradio: {gradio.__version__}')
print(f'NumPy: {numpy.__version__}')
print(f'OpenCV: {cv2.__version__}')
print(f'ONNX Runtime: {onnxruntime.__version__}')
"
```

---

## 📋 Récapitulatif des commandes

**Installation complète recommandée** :
```bash
# 1. FaceFusion
cd facefusion
python install.py
cd ..

# 2. Gradio (interface)
pip install gradio gradio-rangeslider

# 3. Lancer
python actor_faceswap_studio.py
```

**Ou avec le script de lancement** :
```bash
./launch.sh          # macOS/Linux
launch.bat           # Windows
```
Le script gère automatiquement l'installation !

---

## 💡 Conseils

1. **Utilisez un environnement virtuel** (venv) pour éviter les conflits
2. **Python 3.10 ou 3.11** sont les versions les plus stables
3. **Mettez à jour pip** : `pip install --upgrade pip`
4. **Si GPU** : Installez CUDA Toolkit avant onnxruntime-gpu

---

## 🆘 Besoin d'aide ?

Consultez la section **Dépannage** dans [README_APP.md](README_APP.md#-dépannage)

---

**Cette méthode fonctionne dans 99% des cas !** 🎉
