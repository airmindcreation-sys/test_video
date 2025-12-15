# 🎬 Actor Face Swap Studio

Application personnalisée et intuitive pour remplacer le visage d'un acteur dans des vidéos en utilisant l'intelligence artificielle.

Basée sur **FaceFusion**, cette interface simplifiée est spécialement conçue pour le cas d'usage : **portrait d'acteur + vidéos = face swap de qualité professionnelle**.

---

## ✨ Fonctionnalités

- ✅ **Interface simple et intuitive** - Drag & drop pour charger vos fichiers
- ✅ **Presets de qualité** - Rapide, Équilibré, Haute Qualité
- ✅ **Contrôles avancés** - Plus de 10 paramètres ajustables
- ✅ **Support GPU** - CUDA pour traitement rapide (si disponible)
- ✅ **Amélioration faciale** - Face enhancer intégré
- ✅ **Aperçu en temps réel** - Visualisez le résultat immédiatement
- ✅ **13 modèles de swap** - InSwapper, HyperSwap, SimSwap, GhostFace, etc.
- ✅ **Masques intelligents** - Détection automatique des occlusions

---

## 📋 Prérequis

### Système
- **Python 3.10 ou supérieur**
- **8 GB RAM minimum** (16 GB recommandé)
- **GPU NVIDIA avec CUDA** (optionnel mais fortement recommandé pour de bonnes performances)
- **Espace disque**: ~5 GB pour les modèles

### Logiciels requis
- Python 3.10+
- curl (pour le téléchargement des modèles)
- ffmpeg (pour le traitement vidéo)

#### Installation de ffmpeg:

**macOS** (avec Homebrew):
```bash
brew install ffmpeg
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**:
Téléchargez depuis [ffmpeg.org](https://ffmpeg.org/download.html) et ajoutez au PATH

---

## 🚀 Installation

### 1. Cloner ou télécharger ce projet

Vous devriez déjà avoir:
```
for facefusion/
├── facefusion/                    # Dépôt FaceFusion
├── actor_faceswap_studio.py      # Application principale (ce fichier)
├── requirements_app.txt           # Dépendances Python
└── README_APP.md                  # Ce fichier
```

### 2. Installer FaceFusion

```bash
cd facefusion
python install.py
```

Cette commande va:
- Vérifier les dépendances système
- Installer les packages Python nécessaires
- Télécharger les modèles de base

### 3. Installer les dépendances de l'application

```bash
cd ..
pip install -r requirements_app.txt
```

### 4. (Optionnel) Support GPU NVIDIA

Si vous avez une carte graphique NVIDIA avec CUDA:

```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

---

## 🎯 Utilisation

### Lancement de l'application

```bash
python actor_faceswap_studio.py
```

L'interface web s'ouvrira automatiquement dans votre navigateur à l'adresse: `http://localhost:7860`

### Workflow en 4 étapes:

#### 1️⃣ **Charger le portrait de l'acteur**
- Glissez-déposez ou cliquez pour charger une photo
- **Conseils**: Visage bien éclairé, net, face caméra de préférence
- Formats: JPG, PNG, WEBP

#### 2️⃣ **Charger la vidéo cible**
- Glissez-déposez la vidéo où vous voulez insérer le visage
- Formats: MP4, AVI, MOV, MKV, WEBM

#### 3️⃣ **Choisir un preset de qualité**
- **⚡ Rapide**: Pour tests et aperçus (~1-2 min/min de vidéo)
- **⚖️ Équilibré**: Recommandé pour la production (~3-5 min/min)
- **💎 Haute Qualité**: Meilleure qualité possible (~10-15 min/min)

Ou ajustez manuellement dans "Paramètres avancés":
- Modèle de face swap
- Résolution (Pixel Boost)
- Intensité du swap
- Amélioration du visage
- Types de masques
- etc.

#### 4️⃣ **Lancer le traitement**
- Cliquez sur "🚀 Lancer le Face Swap"
- Suivez la progression en temps réel
- Téléchargez le résultat une fois terminé

---

## 🎨 Paramètres détaillés

### Presets de qualité

| Preset | Modèle | Résolution | GPU/CPU | Qualité vidéo | Face Enhancer | Temps (estimation) |
|--------|--------|------------|---------|---------------|---------------|-------------------|
| **⚡ Rapide** | InSwapper 128 | 256 | CPU | 75% | Non | ~1-2 min/min |
| **⚖️ Équilibré** | InSwapper 128 | 512 | GPU préféré | 85% | Oui | ~3-5 min/min |
| **💎 Haute Qualité** | HyperSwap 1A | 1024 | GPU requis | 95% | Oui | ~10-15 min/min |

### Modèles de face swap disponibles

| Modèle | Description | Qualité | Vitesse |
|--------|-------------|---------|---------|
| **inswapper_128** | Rapide et fiable, bon compromis | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| **inswapper_128_fp16** | Version optimisée GPU | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| **hyperswap_1a_256** | Haute qualité, excellent réalisme | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| **hyperswap_1b_256** | Très haute qualité | ⭐⭐⭐⭐⭐ | ⚡⚡ |
| **simswap_256** | Bon équilibre qualité/vitesse | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| **ghost_2_256** | Résultat naturel | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| **blendswap_256** | Fusion douce des visages | ⭐⭐⭐⭐ | ⚡⚡⚡ |

### Pixel Boost (Résolution)

- **256**: Rapide, qualité acceptable pour tests
- **512**: Bon compromis (recommandé)
- **1024**: Haute résolution, meilleur qualité (lent)

### Intensité du swap (Weight)

- **0.5-0.7**: Swap subtil, conserve plus du visage original
- **0.8-0.9**: Équilibré (recommandé)
- **1.0**: Remplacement complet du visage

### Types de masques

- **Occlusion**: Détection automatique des zones occludées (recommandé)
- **Box**: Boîte complète autour du visage
- **Area**: Zone spécifique
- **Region**: Région personnalisée

---

## 💡 Conseils pour de meilleurs résultats

### 📸 Photo source (portrait acteur)
- ✅ Visage bien éclairé et net
- ✅ Face caméra ou angle similaire à la vidéo
- ✅ Haute résolution (minimum 1920x1080)
- ✅ Expression neutre ou correspondant à la vidéo
- ❌ Éviter les photos floues ou mal éclairées
- ❌ Éviter les accessoires qui cachent le visage

### 🎥 Vidéo cible
- ✅ Bonne résolution (1080p ou supérieur)
- ✅ Visage clairement visible
- ✅ Éclairage cohérent
- ❌ Éviter les vidéos avec motion blur excessif
- ❌ Éviter les angles de visage trop différents de la source

### ⚙️ Paramètres
- Commencez avec le preset "**Équilibré**"
- Si le résultat n'est pas naturel, réduisez l'**intensité du swap**
- Activez toujours le **Face Enhancer** pour de meilleurs résultats
- Augmentez le **flou du masque** si les bords sont trop nets
- Testez d'abord sur un court extrait avec le preset "**Rapide**"

---

## 🔧 Dépannage

### ❌ Erreur: "No faces detected"
**Causes possibles**:
- Visage trop petit dans l'image/vidéo
- Angle de visage trop extrême
- Mauvaise qualité d'image

**Solutions**:
- Utilisez une image source avec un visage plus grand
- Essayez un autre détecteur de visage (dans paramètres avancés)
- Améliorez la qualité de la vidéo source

### 💾 Erreur de mémoire (Out of Memory)
**Solutions**:
- Réduisez le **Pixel Boost** (essayez 256 au lieu de 512)
- Utilisez le preset "**Rapide**"
- Fermez les autres applications
- Désactivez le **Face Enhancer**

### ⏱️ Traitement très lent
**Solutions**:
- Vérifiez que vous utilisez le GPU (provider = cuda)
- Installez `onnxruntime-gpu` si vous avez une carte NVIDIA
- Utilisez un preset plus rapide
- Réduisez la résolution de la vidéo

### 🎭 Résultat pas naturel
**Solutions**:
- Réduisez l'**intensité du swap** (0.7-0.8 au lieu de 1.0)
- Activez le **Face Enhancer**
- Essayez un autre **modèle** (GhostFace ou SimSwap)
- Augmentez le **flou du masque** (0.5-0.7)
- Vérifiez que l'éclairage de la photo source correspond à la vidéo

### 🚫 L'application ne se lance pas
**Solutions**:
```bash
# Vérifiez votre version de Python
python --version  # Doit être 3.10+

# Réinstallez les dépendances
pip install -r requirements_app.txt --force-reinstall

# Vérifiez ffmpeg
ffmpeg -version

# Vérifiez les logs
python actor_faceswap_studio.py
```

---

## 📂 Structure des dossiers

```
for facefusion/
├── facefusion/                    # FaceFusion (core)
│   ├── facefusion/               # Modules Python
│   ├── .models/                  # Modèles téléchargés (créé auto)
│   └── ...
├── uploads/                       # Photos sources uploadées (créé auto)
├── outputs/                       # Vidéos traitées (créé auto)
├── temp/                          # Fichiers temporaires (créé auto)
├── actor_faceswap_studio.py      # Application principale
├── requirements_app.txt           # Dépendances
├── README_APP.md                  # Documentation
└── launch.sh / launch.bat         # Scripts de lancement
```

Les dossiers `uploads/`, `outputs/` et `temp/` sont créés automatiquement au premier lancement.

---

## 🎓 FAQ

### Q: Combien de temps prend un traitement ?
**R**: Cela dépend de:
- Durée de la vidéo
- Preset choisi
- Présence d'un GPU

Avec GPU NVIDIA (CUDA):
- Rapide: ~1-2 min par minute de vidéo
- Équilibré: ~3-5 min par minute
- Haute qualité: ~10-15 min par minute

Sans GPU (CPU uniquement): **2-5x plus lent**

### Q: Puis-je traiter plusieurs vidéos à la suite ?
**R**: Oui, traitez-les une par une dans l'interface. Pour du batch processing automatisé, vous pouvez utiliser FaceFusion directement en ligne de commande.

### Q: Les modèles sont téléchargés automatiquement ?
**R**: Oui, la première fois que vous utilisez un modèle, il sera téléchargé automatiquement. Les modèles font entre 100 MB et 500 MB.

### Q: Puis-je utiliser cette app sans GPU ?
**R**: Oui, mais le traitement sera beaucoup plus lent. Utilisez le preset "Rapide" et testez sur de courts extraits.

### Q: Est-ce que ça fonctionne sur plusieurs visages dans la vidéo ?
**R**: Par défaut, l'application swap le premier visage détecté. FaceFusion supporte le multi-face, mais cette interface simplifiée se concentre sur un seul visage.

### Q: Où sont sauvegardés mes résultats ?
**R**: Dans le dossier `outputs/` avec le nom `faceswap_[nom_video]_[preset].mp4`

### Q: Puis-je partager mon interface en ligne ?
**R**: Oui, dans le code de `actor_faceswap_studio.py`, changez `share=False` en `share=True` dans la méthode `app.launch()`. Gradio générera un lien public temporaire.

---

## 🛠️ Développement et personnalisation

### Modifier les presets

Éditez la classe `FaceSwapConfig` dans [actor_faceswap_studio.py:45-75](actor_faceswap_studio.py#L45-L75):

```python
PRESETS = {
    'mon_preset': {
        'name': '🔥 Mon Preset',
        'description': 'Description de mon preset',
        'face_swapper_model': 'inswapper_128',
        'face_swapper_pixel_boost': '512',
        # ... autres paramètres
    }
}
```

### Ajouter de nouveaux modèles

Les modèles disponibles sont définis dans FaceFusion. Consultez la documentation officielle: https://docs.facefusion.io

### Personnaliser l'interface

L'interface utilise **Gradio**. Modifiez la fonction `create_gradio_interface()` dans [actor_faceswap_studio.py:200-550](actor_faceswap_studio.py#L200-L550).

Documentation Gradio: https://gradio.app/docs/

---

## 📜 Licence

Cette application est une surcouche basée sur **FaceFusion**.

- **FaceFusion**: OpenRAIL-AS License (voir `facefusion/LICENSE.md`)
- **Cette application**: Libre d'utilisation pour usage personnel et commercial

**Important**: Respectez les lois locales sur le droit à l'image et obtenez les autorisations nécessaires avant de manipuler des visages de personnes réelles.

---

## 🤝 Support

### Problèmes avec cette application
- Ouvrez une issue sur GitHub ou contactez le développeur

### Problèmes avec FaceFusion
- Documentation officielle: https://docs.facefusion.io
- GitHub: https://github.com/facefusion/facefusion

---

## 🎉 Crédits

- **FaceFusion**: https://github.com/facefusion/facefusion
- **Gradio**: https://gradio.app
- **Modèles de face swap**: InsightFace, FaceFusion Research, Ai-Forever, GuijiAI, et autres

---

<center>

**Fait avec ❤️ pour simplifier le face swapping d'acteurs**

</center>
