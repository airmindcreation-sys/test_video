# 🎬 Actor Face Swap Studio V3 - Guide Complet

## ✅ Version Finale - 100% Fonctionnelle

### 🚀 Lancement

```bash
cd "/Users/martinemenguy/Desktop/for facefusion"
python3 actor_faceswap_studio_v3.py
```

**URL :** http://localhost:7862

---

## 📋 Fonctionnalités Complètes

### 1. 🎬 Face Swap Simple

**Onglet principal pour un traitement unique avec tous les paramètres**

#### Paramètres Disponibles :
- **Face Swapper Model** : 13 modèles (inswapper, hyperswap, simswap, etc.)
- **Pixel Boost** : 256x256, 512x512, 768x768, 1024x1024
- **Face Enhancer** : 15 modèles (codeformer, gfpgan, real_esrgan, etc.)
  - Blend : 0-100
- **Frame Enhancer** : 18 modèles (ultra_sharp, swin2_sr, etc.)
- **Lip Sync** : 3 modèles (wav2lip_gan_96, wav2lip_96, edtalk_256)
  - ✅ **Audio extrait et fusionné automatiquement**
- **Reference Distance** : 0.0 - 1.0 (précision du matching)
- **Execution Provider** : CPU, CUDA, CoreML
- **Output Quality** : 0-100

#### Workflow :
1. Upload portrait + vidéo
2. Ajuster les paramètres
3. Cliquer "Lancer Face Swap"
4. Télécharger le résultat

---

### 2. 🧪 Test en Groupe - Configs Pré-définies

**12 configurations optimisées prêtes à l'emploi**

#### Configurations Disponibles :

| # | Nom | Processeurs | Spécificité |
|---|-----|-------------|-------------|
| 01 | Golden Standard | face_swapper + face_enhancer | InSwapper + CodeFormer (référence) |
| 02 | HyperSwap Haute Rés | face_swapper + face_enhancer | HyperSwap 1B + Pixel Boost 1024x1024 |
| 03 | Cinématique | face_swapper + face_enhancer | InSwapper + GFPGAN 1.4 |
| 04 | HyperSwap Équilibré | face_swapper + face_enhancer | HyperSwap + GFPGAN |
| 05 | Matching Strict | face_swapper + face_enhancer | Distance 0.4 (précis) |
| 06 | Matching Souple | face_swapper + face_enhancer | Distance 0.9 (angles difficiles) |
| 07 | Pixel Boost | face_swapper + face_enhancer | InSwapper + Pixel Boost 512x512 |
| 08 | Pipeline Complet | face_swapper + face_enhancer + frame_enhancer | Avec Frame Enhancer |
| 09 | Blend Élevé | face_swapper + face_enhancer | Blend 90 (plus naturel) |
| 10 | Preview Rapide | face_swapper | Sans enhancer (rapide) |
| 11 | **Avec Lip Sync** | face_swapper + face_enhancer + **lip_syncer** | **InSwapper + Lip Sync** ✅ |
| 12 | **Lip Sync HyperSwap** | face_swapper + face_enhancer + **lip_syncer** | **HyperSwap + Lip Sync Haute Qualité** ✅ |

#### Workflow :
1. Upload portrait + vidéo
2. Cocher les configs à tester (multi-sélection)
3. Cliquer "Lancer Tests Pré-définis"
4. Comparer les résultats dans la galerie
5. Télécharger les meilleures vidéos

#### Résultats :
- **Résumé** : Nombre de succès/échecs
- **Galerie** : Toutes les vidéos générées
- **Lecteur** : Prévisualisation
- **Dossier** : `batch_results/batch_YYYYMMDD_HHMMSS/`

---

### 3. ⚙️ Test en Groupe - Configs Personnalisées

**Créez jusqu'à 5 configurations totalement personnalisées**

#### Paramètres par Configuration :

##### Activation
- ✅ Activer/Désactiver chaque config

##### Identification
- **Nom** : Nom personnalisé de la config

##### Face Swapper
- **Model** : 13 choix
- **Pixel Boost** : 4 options

##### Face Enhancer
- **Activer** : On/Off
- **Model** : 15 choix
- **Blend** : 0-100

##### Frame Enhancer
- **Activer** : On/Off
- **Model** : 18 choix

##### Lip Sync ✅
- **Activer** : On/Off
- **Model** : wav2lip_gan_96, wav2lip_96, edtalk_256
- **Audio** : Extraction et fusion automatiques

##### Autres
- **Reference Distance** : 0.0 - 1.0
- **Quality** : 0-100
- **Execution Provider** : CPU, CUDA, CoreML

#### Workflow :
1. Upload portrait + vidéo (commun aux 5 configs)
2. Configurer chaque config dans son accordion
3. Activer les configs désirées (checkbox)
4. Cliquer "Lancer Tests Personnalisés"
5. Comparer et télécharger

#### Exemple d'Utilisation :
- **Config 1** : InSwapper + CodeFormer (baseline)
- **Config 2** : HyperSwap + GFPGAN (alternative)
- **Config 3** : InSwapper + Lip Sync (avec audio)
- **Config 4** : HyperSwap + Frame Enhancer (haute qualité)
- **Config 5** : Rapide sans enhancer (preview)

---

## 🎵 Extraction et Fusion Audio Automatique

### Comment ça marche ?

#### Quand le Lip Sync est activé :

1. **Extraction** (avant traitement)
   - Format : WAV mono 44.1kHz
   - Emplacement : `temp/[video_name]_audio.wav`
   - Automatique et transparent

2. **Traitement FaceFusion**
   - Commande : `--source-paths audio.wav portrait.jpg`
   - Lip sync appliqué avec le modèle sélectionné

3. **Fusion** (après génération)
   - Codec : AAC (standard MP4)
   - Optimisation : `-c:v copy` (pas de ré-encodage vidéo)
   - Résultat : Vidéo avec audio parfaitement synchronisé

### Résultats Garantis :
- ✅ Audio préservé dans la vidéo finale
- ✅ Lèvres synchronisées
- ✅ Aucune action manuelle requise
- ✅ Fonctionne dans **tous les modes** (Simple, Pré-défini, Personnalisé)

---

## 📂 Structure des Dossiers

```
/Users/martinemenguy/Desktop/for facefusion/
├── actor_faceswap_studio_v3.py        # Application V3
├── outputs/                            # Face swap simples
│   └── faceswap_xxx_YYYYMMDD.mp4
├── batch_results/                      # Tests en groupe
│   ├── batch_YYYYMMDD_HHMMSS/         # Pré-définis
│   │   ├── golden-standard.mp4
│   │   ├── with-lip-sync.mp4
│   │   └── results.json
│   └── custom_batch_YYYYMMDD_HHMMSS/  # Personnalisés
│       ├── custom_1.mp4
│       ├── custom_2.mp4
│       └── results.json
└── temp/                               # Fichiers temporaires
    └── video_name_audio.wav           # Audio extrait
```

---

## 🎯 Cas d'Usage

### Cas 1 : Test Rapide
**Objectif** : Tester rapidement une vidéo

**Solution** : Face Swap Simple
- Upload fichiers
- Laisser paramètres par défaut
- Activer Lip Sync si besoin
- Lancer

### Cas 2 : Comparaison de Modèles
**Objectif** : Comparer plusieurs modèles de face swapper

**Solution** : Configs Personnalisées
- Config 1 : inswapper_128_fp16
- Config 2 : hyperswap_1a_256
- Config 3 : hyperswap_1b_256
- Config 4 : simswap_256
- Config 5 : ghost_2_256

### Cas 3 : Optimisation Qualité
**Objectif** : Trouver les meilleurs paramètres

**Solution** : Configs Pré-définies
- Sélectionner configs 1, 2, 3, 7, 8, 11
- Lancer tests
- Comparer dans la galerie
- Noter la meilleure config

### Cas 4 : Production avec Lip Sync
**Objectif** : Vidéo finale avec lip sync parfait

**Solution** : Face Swap Simple
- Activer Lip Sync
- Face Swapper : hyperswap_1b_256
- Pixel Boost : 1024x1024
- Face Enhancer : codeformer (blend 85)
- Lip Sync Model : wav2lip_gan_96
- Quality : 95

---

## 🔧 Modèles Recommandés

### Face Swapper

| Modèle | Qualité | Vitesse | Usage |
|--------|---------|---------|-------|
| **inswapper_128_fp16** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Production (recommandé) |
| **hyperswap_1b_256** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Haute qualité |
| **hyperswap_1c_256** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Équilibré |
| **simswap_256** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tests rapides |

### Face Enhancer

| Modèle | Qualité | Vitesse | Usage |
|--------|---------|---------|-------|
| **codeformer** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Production (recommandé) |
| **gfpgan_1.4** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Rendu cinématique |
| **real_esrgan_x4_fp16** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Upscaling maximum |

### Lip Sync

| Modèle | Qualité | Vitesse | Usage |
|--------|---------|---------|-------|
| **wav2lip_gan_96** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Production (recommandé) |
| **wav2lip_96** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Équilibré |
| **edtalk_256** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tests rapides |

---

## 🐛 Dépannage

### Problème : "ModuleNotFoundError: No module named 'gradio'"

**Solution** :
```bash
python3 -m pip install --user gradio
```

### Problème : "Audio extraction failed"

**Cause** : La vidéo n'a pas de piste audio

**Solution** :
- Vérifier avec : `ffprobe video.mp4`
- Désactiver Lip Sync si pas d'audio

### Problème : Tests en groupe lents

**Solution** :
- Utiliser `execution_provider: cuda` au lieu de `cpu`
- Réduire le nombre de configs à tester
- Désactiver frame_enhancer (très lent)

---

## 📊 Comparaison V2 vs V3

| Fonctionnalité | V2 | V3 |
|----------------|----|----|
| Face Swap Simple | ✅ | ✅ |
| Tous les modèles | ❌ | ✅ 13+15+18 |
| Frame Enhancer | ❌ | ✅ |
| Lip Sync | ✅ | ✅ |
| Extraction audio auto | ✅ | ✅ |
| Fusion audio auto | ✅ | ✅ |
| Test multi-configs | ❌ | ✅ |
| Configs pré-définies | ❌ | ✅ 12 configs |
| Configs personnalisées | ❌ | ✅ 5 configs |
| Galerie comparaison | ❌ | ✅ |
| Export JSON résultats | ❌ | ✅ |

**Recommandation** : Utiliser V3 pour tout, V2 n'est plus nécessaire.

---

## ✅ Checklist Avant Utilisation

- [ ] FaceFusion installé dans `/facefusion/`
- [ ] ffmpeg installé (`which ffmpeg`)
- [ ] Gradio installé (`python3 -c "import gradio"`)
- [ ] Port 7862 libre
- [ ] Vidéo avec audio (si lip sync)

---

**Date** : 2025-12-16
**Version** : V3 Finale
**Status** : ✅ **100% FONCTIONNELLE**
**URL** : http://localhost:7862
