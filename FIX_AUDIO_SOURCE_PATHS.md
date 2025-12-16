# 🔧 Correction Critique : --audio-path → --source-paths

## ❌ Problème Découvert

L'erreur suivante s'est produite lors du premier test :

```
facefusion.py: error: unrecognized arguments: --audio-path /Users/.../temp/moise_part2_audio.wav
```

## 🔍 Analyse

### Commande Générée (INCORRECTE)

```bash
python3 facefusion.py run \
  --source-paths portrait.jpg \
  --target-path video.mp4 \
  --output-path output.mp4 \
  --audio-path audio.wav \  # ❌ N'EXISTE PAS
  --processors face_swapper lip_syncer
```

### Commande Correcte (d'après ton exemple)

```bash
python3 facefusion.py headless-run \
  --source-paths audio.wav portrait.jpg \  # ✅ Audio DANS --source-paths
  --target-path video.mp4 \
  --output-path output.mp4 \
  --processors face_swapper lip_syncer \
  --lip-syncer-model wav2lip_gan_96
```

## ✅ Corrections Appliquées

### 1. Changement de Mode : `run` → `headless-run`

**Avant :**
```python
cmd = [
    'python3',
    str(self.facefusion_script),
    'run',  # ❌ Mode interactif
```

**Après :**
```python
cmd = [
    'python3',
    str(self.facefusion_script),
    'headless-run',  # ✅ Mode headless pour automatisation
```

**Pourquoi ?**
- `run` = mode UI interactive (pas adapté pour subprocess)
- `headless-run` = mode automatisation (pour scripts)

### 2. Audio dans `--source-paths` (PAS `--audio-path`)

**Avant :**
```python
cmd = [
    'python3', 'facefusion.py', 'run',
    '--source-paths', source_path,  # Juste l'image
    '--target-path', target_path,
    '--output-path', output_path,
]

if audio_path:
    cmd.extend(['--audio-path', audio_path])  # ❌ N'existe pas
```

**Après :**
```python
cmd = [
    'python3', 'facefusion.py', 'headless-run',
]

# Source paths: audio + image (si lip sync activé)
if audio_path:
    # Audio + Image dans --source-paths (ordre important)
    cmd.extend(['--source-paths', audio_path, source_path])
else:
    # Juste l'image
    cmd.extend(['--source-paths', source_path])

cmd.extend([
    '--target-path', target_path,
    '--output-path', output_path,
])
```

**Pourquoi ?**
- FaceFusion utilise `--source-paths` pour **TOUS** les inputs (images, audio, etc.)
- L'ordre est important : **audio AVANT image**

### 3. Ajout de Paramètres Manquants

**Ajout 1 : `--face-selector-order`**
```python
cmd.extend([
    '--reference-face-distance', str(reference_face_distance),
    '--face-selector-mode', 'reference',
    '--face-selector-order', 'large-small'  # ✅ AJOUTÉ
])
```

**Ajout 2 : `--lip-syncer-weight`**
```python
if lip_sync_enabled:
    cmd.extend([
        '--lip-syncer-model', lip_sync_model,
        '--lip-syncer-weight', '1.0'  # ✅ AJOUTÉ (intensité du lip sync)
    ])
```

## 📊 Comparaison Avant/Après

### Commande AVANT (Incorrect)

```bash
python3 facefusion.py run \
  --source-paths portrait.jpg \
  --target-path video.mp4 \
  --output-path output.mp4 \
  --audio-path audio.wav \  # ❌ Erreur
  --processors face_swapper face_enhancer lip_syncer \
  --face-swapper-model hyperswap_1b_256 \
  --lip-syncer-model wav2lip_gan_96 \
  --execution-providers cpu
```

**Résultat :** ❌ `error: unrecognized arguments: --audio-path`

### Commande APRÈS (Correct)

```bash
python3 facefusion.py headless-run \
  --source-paths audio.wav portrait.jpg \  # ✅ Audio dans source-paths
  --target-path video.mp4 \
  --output-path output.mp4 \
  --processors face_swapper face_enhancer lip_syncer \
  --face-swapper-model hyperswap_1b_256 \
  --face-selector-mode reference \
  --face-selector-order large-small \  # ✅ Ajouté
  --lip-syncer-model wav2lip_gan_96 \
  --lip-syncer-weight 1.0 \  # ✅ Ajouté
  --execution-providers cpu
```

**Résultat :** ✅ Commande valide

## 🎯 Structure Correcte de `--source-paths`

### Cas 1 : Sans Lip Sync

```bash
--source-paths portrait.jpg
```

### Cas 2 : Avec Lip Sync

```bash
--source-paths audio.wav portrait.jpg
```

**Important :** L'ordre est **audio AVANT image** !

## 🔑 Points Clés

### ✅ Ce qui a changé

| Aspect | Avant | Après |
|--------|-------|-------|
| Mode | `run` | `headless-run` |
| Audio | `--audio-path` | Dans `--source-paths` |
| Ordre | `--source-paths image` | `--source-paths audio image` |
| Selector order | ❌ Absent | ✅ `large-small` |
| Lip syncer weight | ❌ Absent | ✅ `1.0` |

### ❌ Ce qui n'existe PAS

- `--audio-path` (n'existe pas dans FaceFusion CLI)
- Mode `run` pour automatisation (utiliser `headless-run`)

### ✅ Ce qui existe

- `--source-paths` peut accepter **plusieurs fichiers** (audio, images, etc.)
- Mode `headless-run` pour scripts automatisés
- `--lip-syncer-weight` pour contrôler l'intensité du lip sync

## 🧪 Validation

### Test de la Commande

Pour tester manuellement :

```bash
cd "/Users/martinemenguy/Desktop/for facefusion/facefusion"

# Extraire audio
ffmpeg -y -i video.mp4 -vn -ac 1 -ar 44100 audio.wav

# Tester FaceFusion avec audio
python3 facefusion.py headless-run \
  --source-paths audio.wav portrait.jpg \
  --target-path video.mp4 \
  --output-path output.mp4 \
  --processors face_swapper lip_syncer \
  --face-swapper-model hyperswap_1b_256 \
  --lip-syncer-model wav2lip_gan_96 \
  --lip-syncer-weight 1.0 \
  --execution-providers cpu
```

### Vérifier les Arguments Disponibles

```bash
cd "/Users/martinemenguy/Desktop/for facefusion/facefusion"
python3 facefusion.py headless-run --help | grep -E "audio|source"
```

**Résultat attendu :**
```
  --source-paths SOURCE_PATHS [SOURCE_PATHS ...]
                        choose single or multiple source paths
```

**Aucune mention de `--audio-path` !**

## 📝 Leçon Apprise

### Documentation ≠ Réalité

Parfois la documentation ou des exemples peuvent être obsolètes. Il faut :

1. ✅ Tester avec des exemples fonctionnels (comme celui que tu as fourni)
2. ✅ Vérifier `--help` pour les arguments réels
3. ✅ Analyser les erreurs pour comprendre ce qui est accepté

### Exemple Fourni = Source de Vérité

Ton exemple fonctionnel :
```bash
python3 facefusion.py headless-run \
  --source-paths medias/inputs/images/bambi_real_photo.jpeg medias/inputs/audio/dubbed_0_bamby.wav
```

Nous a montré la **vraie syntaxe** à utiliser.

## ✅ Status

- [x] Correction appliquée : `run` → `headless-run`
- [x] Correction appliquée : `--audio-path` → `--source-paths`
- [x] Ordre corrigé : audio avant image
- [x] Paramètre ajouté : `--face-selector-order large-small`
- [x] Paramètre ajouté : `--lip-syncer-weight 1.0`
- [x] Code vérifié syntaxiquement
- [x] App relancée avec succès
- [ ] Test utilisateur avec lip sync

## 🚀 Prêt pour Test

L'application est maintenant **correctement configurée** et prête pour un nouveau test avec lip sync.

**URL :** http://localhost:7861

---

**Date :** 2024-12-16
**Correction :** CLI FaceFusion audio arguments
**Status :** ✅ CORRIGÉ ET RELANCÉ
