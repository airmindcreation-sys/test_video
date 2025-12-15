# 📂 Structure du Projet - Actor Face Swap Studio

## Vue d'ensemble

```
for facefusion/
│
├── 🎬 FICHIERS PRINCIPAUX DE L'APPLICATION
│   ├── actor_faceswap_studio.py       # Application principale (interface Gradio)
│   ├── requirements_app.txt            # Dépendances Python de l'app
│   ├── launch.sh                       # Script de lancement (macOS/Linux)
│   ├── launch.bat                      # Script de lancement (Windows)
│   └── .gitignore                      # Fichiers à ignorer par Git
│
├── 📚 DOCUMENTATION
│   ├── README_APP.md                   # Documentation complète de l'application
│   ├── GUIDE_DEMARRAGE_RAPIDE.md      # Guide de démarrage en 10 minutes
│   └── STRUCTURE_DU_PROJET.md         # Ce fichier (structure du projet)
│
├── 🧠 FACEFUSION (dépendance)
│   └── facefusion/                     # Dépôt FaceFusion (core engine)
│       ├── facefusion/                 # Modules Python
│       │   ├── core.py                # Point d'entrée CLI
│       │   ├── program.py             # Gestion des arguments
│       │   ├── processors/            # Processeurs (face_swapper, etc.)
│       │   ├── workflows/             # Workflows (image_to_video, etc.)
│       │   └── uis/                   # Interface Gradio de FaceFusion
│       ├── facefusion.py              # Exécutable principal
│       ├── install.py                 # Script d'installation
│       ├── requirements.txt           # Dépendances FaceFusion
│       └── .models/                   # Modèles IA (créé automatiquement)
│
└── 💾 DOSSIERS DE DONNÉES (créés automatiquement)
    ├── uploads/                        # Photos sources uploadées
    ├── outputs/                        # Vidéos traitées (résultats)
    └── temp/                           # Fichiers temporaires de traitement
```

---

## 📄 Description détaillée des fichiers

### 🎬 Fichiers principaux

#### [actor_faceswap_studio.py](actor_faceswap_studio.py)
**Rôle**: Application principale avec interface Gradio personnalisée

**Contient**:
- `FaceSwapConfig`: Configuration des presets et modèles
- `FaceSwapProcessor`: Classe de traitement du face swap
- `create_gradio_interface()`: Création de l'interface utilisateur
- `main()`: Point d'entrée de l'application

**Lignes de code**: ~550 lignes

**Fonctionnalités**:
- Interface web intuitive à 3 colonnes
- 3 presets de qualité (Rapide, Équilibré, Haute Qualité)
- Paramètres avancés ajustables
- Validation des entrées
- Gestion des erreurs
- Barre de progression en temps réel

#### [requirements_app.txt](requirements_app.txt)
**Rôle**: Liste des dépendances Python pour l'application

**Dépendances principales**:
- `gradio>=5.44.1` - Framework d'interface web
- `numpy>=2.2.6` - Calculs numériques
- `onnxruntime>=1.23.2` - Moteur d'inférence IA
- `opencv-python>=4.12.0.88` - Traitement d'images/vidéos
- `scipy>=1.16.3` - Algorithmes scientifiques

#### [launch.sh](launch.sh) / [launch.bat](launch.bat)
**Rôle**: Scripts de lancement automatique de l'application

**Fonctionnalités**:
- Vérification de Python 3.10+
- Vérification de ffmpeg
- Vérification de FaceFusion
- Installation automatique des dépendances si manquantes
- Lancement de l'application

---

### 📚 Documentation

#### [README_APP.md](README_APP.md)
**Contenu**: Documentation complète (3500+ mots)
- Installation détaillée
- Guide d'utilisation
- Description des paramètres
- Conseils pour de meilleurs résultats
- Dépannage
- FAQ

#### [GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md)
**Contenu**: Guide express pour démarrer en 10-15 minutes
- Checklist pré-installation
- Installation en 3 étapes
- Premier test guidé
- Conseils de workflow

#### [STRUCTURE_DU_PROJET.md](STRUCTURE_DU_PROJET.md)
**Contenu**: Ce fichier - Architecture complète du projet

---

## 🧠 Architecture de l'application

### Flux de traitement

```
┌─────────────────────────────────────────────────────────┐
│  1. Interface Gradio (actor_faceswap_studio.py)        │
│     ↓                                                    │
│     • Upload photo source                               │
│     • Upload vidéo cible                                │
│     • Sélection des paramètres                          │
│     • Clic sur "Lancer le Face Swap"                    │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  2. FaceSwapProcessor.process_video()                   │
│     ↓                                                    │
│     • Validation des fichiers                           │
│     • Application du preset                             │
│     • Configuration de FaceFusion                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  3. FaceFusion Core (facefusion/workflows)              │
│     ↓                                                    │
│     • Détection des visages (face_detector)             │
│     • Extraction des embeddings (face_analyser)         │
│     • Face swap (processors/face_swapper)               │
│     • Amélioration (processors/face_enhancer)           │
│     • Encodage vidéo (ffmpeg)                           │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  4. Résultat                                             │
│     ↓                                                    │
│     • Sauvegarde dans outputs/                          │
│     • Affichage dans l'interface                        │
│     • Téléchargement disponible                         │
└─────────────────────────────────────────────────────────┘
```

### Intégration avec FaceFusion

L'application utilise FaceFusion comme **moteur de traitement** en important directement ses modules Python:

```python
# Imports clés depuis FaceFusion
from facefusion import state_manager, logger
from facefusion.args import apply_args
from facefusion.workflows import image_to_video
from facefusion.processors.core import get_processors_modules
from facefusion.execution import get_available_execution_providers
```

**Avantages de cette approche**:
- Pas de duplication de code
- Mises à jour FaceFusion automatiques
- Accès à tous les modèles et processeurs
- Configuration flexible via `state_manager`

---

## 💾 Dossiers de données

### `uploads/` (créé automatiquement)
**Contenu**: Photos sources uploadées temporairement
**Nettoyage**: Manuel ou automatique selon configuration

### `outputs/` (créé automatiquement)
**Contenu**: Vidéos traitées (résultats finaux)
**Format de nom**: `faceswap_[nom_video]_[preset].mp4`
**Exemple**: `faceswap_myvideo_equilibre.mp4`

### `temp/` (créé automatiquement)
**Contenu**: Fichiers temporaires de traitement
- Frames extraits de la vidéo
- Fichiers intermédiaires
**Nettoyage**: Automatique après chaque traitement

---

## 🎨 Personnalisation

### Modifier les presets

Éditez la classe `FaceSwapConfig` dans [actor_faceswap_studio.py](actor_faceswap_studio.py#L45):

```python
PRESETS = {
    'mon_preset_custom': {
        'name': '🔥 Mon Preset',
        'description': 'Description personnalisée',
        'face_swapper_model': 'inswapper_128',
        'face_swapper_pixel_boost': '768',  # Valeur custom
        'execution_providers': ['cuda'],
        'output_video_quality': 90,
        'face_enhancer_enabled': True
    }
}
```

### Ajouter des fonctionnalités

L'architecture modulaire permet d'ajouter facilement:

1. **Nouveaux processeurs FaceFusion**:
```python
config['processors'].append('expression_restorer')
config['expression_restorer_model'] = 'expression_restorer_v1'
```

2. **Batch processing**: Modifier `FaceSwapProcessor` pour traiter plusieurs vidéos

3. **Templates de configuration**: Sauvegarder/charger des configurations

4. **Historique**: Logger les traitements dans une base de données

---

## 🔧 Technologies utilisées

### Frontend (Interface)
- **Gradio 5.44+**: Framework d'interface web
  - Thème personnalisé (Soft)
  - Components: Image, Video, Slider, Dropdown, Checkbox
  - CSS personnalisé pour le styling

### Backend (Traitement)
- **FaceFusion**: Moteur de face swap
  - 13 modèles de swap disponibles
  - Workflows: image_to_video
  - Processeurs: face_swapper, face_enhancer, etc.

### Inférence IA
- **ONNX Runtime**: Exécution des modèles
  - Support CPU
  - Support GPU (CUDA, TensorRT, DirectML, CoreML)
- **OpenCV**: Traitement d'images et vidéos
- **NumPy/SciPy**: Calculs numériques

### Encodage vidéo
- **FFmpeg**: Encodage/décodage vidéo
  - Codecs: H.264, H.265, VP9
  - Audio: AAC, MP3, FLAC

---

## 📊 Statistiques du projet

| Élément | Quantité |
|---------|----------|
| Fichiers Python | 1 principal |
| Lignes de code | ~550 lignes |
| Fichiers de documentation | 4 fichiers |
| Presets inclus | 3 (Rapide, Équilibré, Haute Qualité) |
| Modèles supportés | 13 modèles de face swap |
| Processeurs disponibles | 12+ (via FaceFusion) |
| Langues d'interface | Français (peut être traduit) |

---

## 🚀 Évolutions possibles

### Court terme
- [ ] Ajout d'un système de templates de configuration
- [ ] Historique des traitements effectués
- [ ] Prévisualisation sur une frame avant traitement complet
- [ ] Support multi-visages

### Moyen terme
- [ ] Batch processing (traiter plusieurs vidéos)
- [ ] API REST pour intégration externe
- [ ] Système de queue pour traiter plusieurs jobs
- [ ] Mode "Before/After" pour comparaison

### Long terme
- [ ] Interface multilingue
- [ ] Base de données des traitements
- [ ] Authentification utilisateur
- [ ] Cloud deployment (AWS, GCP, Azure)
- [ ] Application desktop (Electron/PyQt)

---

## 🔗 Liens utiles

- **FaceFusion GitHub**: https://github.com/facefusion/facefusion
- **FaceFusion Docs**: https://docs.facefusion.io
- **Gradio Documentation**: https://gradio.app/docs/
- **ONNX Runtime**: https://onnxruntime.ai/

---

<center>

**Structure créée pour simplicité et extensibilité**

</center>
