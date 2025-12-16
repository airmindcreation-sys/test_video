# 🧪 Plan de Test - Workflow Lip Sync Automatique

## Objectif

Valider que l'extraction et la fusion audio fonctionnent correctement avec le lip sync.

## Prérequis

- [x] ffmpeg installé et dans le PATH
- [ ] Vidéo de test **avec audio** (format MP4, WebM, ou AVI)
- [ ] Photo d'acteur (format JPG ou PNG)
- [ ] Application V2 lancée

## Test 1: Lip Sync Activé (Workflow Complet)

### Étapes

1. **Lancer l'application**
   ```bash
   cd "/Users/martinemenguy/Desktop/for facefusion"
   python3 actor_faceswap_studio_v2.py
   ```

2. **Ouvrir dans le navigateur**
   - URL: http://localhost:7861

3. **Upload des fichiers**
   - Photo: `actor.jpg` (portrait)
   - Vidéo: `video_with_audio.mp4` (avec piste audio)

4. **Configuration**
   - Preset: **Équilibré** (recommandé)
   - Lip Sync: **✅ Activé** (cocher la case)
   - Lip Sync Model: `wav2lip_gan_96` (par défaut)

5. **Lancer le traitement**
   - Cliquer sur "Lancer le Face Swap"

### Résultats Attendus

#### Dans les logs (terminal)

```
🔍 Validation des fichiers...
🎵 Extraction de l'audio pour le lip sync...  # ← NOUVEAU
⚙️ Construction de la commande...

🚀 Commande FaceFusion:
   python3 facefusion.py run --source-paths ... --audio-path temp/video_with_audio_audio.wav ...  # ← --audio-path présent

🎬 Lancement du traitement FaceFusion...
🎭 Traitement en cours...
🎬 Traitement des frames...
🎥 Encodage de la vidéo...
🎉 Finalisation...
🔊 Fusion de l'audio final...  # ← NOUVEAU
✅ Terminé!
```

#### Dans l'interface Gradio

- Barre de progression affiche: `🔊 Fusion de l'audio final...`
- Message de succès:
  ```
  ✅ Face swap terminé avec succès !
  📁 Fichier: faceswap_video_with_audio_equilibre.mp4
  💾 Taille: XX.XX MB
  📂 Dossier: outputs
  🎤 Lip sync activé
  ```

#### Fichiers générés

```
outputs/
└── faceswap_video_with_audio_equilibre.mp4  (vidéo finale avec audio)

temp/
└── video_with_audio_audio.wav  (audio extrait)
```

#### Validation de la vidéo finale

1. **Ouvrir la vidéo** dans un lecteur (VLC, QuickTime, etc.)
2. **Vérifier**:
   - [x] L'audio est présent
   - [x] Les lèvres sont synchronisées avec l'audio
   - [x] Le visage a été remplacé
   - [x] La qualité est correcte

---

## Test 2: Lip Sync Désactivé (Sans Audio)

### Étapes

1. Upload fichiers (même vidéo avec audio)
2. Configuration:
   - Preset: **Équilibré**
   - Lip Sync: **❌ Désactivé** (décocher)
3. Lancer

### Résultats Attendus

#### Dans les logs

```
🔍 Validation des fichiers...
⚙️ Construction de la commande...  # PAS d'extraction audio

🚀 Commande FaceFusion:
   python3 facefusion.py run --source-paths ... --processors face_swapper face_enhancer ...
   # PAS de --audio-path
   # PAS de lip_syncer dans --processors

✅ Terminé!
```

#### Validation

- Vidéo générée **sans** lip sync
- Audio préservé de la vidéo originale (comportement par défaut de FaceFusion)
- Pas d'extraction audio dans `temp/`

---

## Test 3: Erreur - Vidéo Sans Audio

### Étapes

1. Upload vidéo **sans piste audio** (ex: vidéo muette)
2. Configuration:
   - Lip Sync: **✅ Activé**
3. Lancer

### Résultats Attendus

#### Message d'erreur

```
❌ Échec de l'extraction audio pour le lip sync. Vérifiez que la vidéo contient une piste audio.
```

#### Dans les logs

```
🎵 Extraction de l'audio pour le lip sync...
❌ Extraction audio échouée: fichier vide
(ou: ❌ Extraction audio échouée: [stderr ffmpeg])
```

#### Comportement

- Traitement **interrompu** avant d'appeler FaceFusion
- Aucun fichier généré
- Message clair pour l'utilisateur

---

## Test 4: Différents Formats Audio

Tester avec vidéos ayant différents codecs audio:

| Format Vidéo | Codec Audio | Résultat Attendu |
|--------------|-------------|------------------|
| MP4          | AAC         | ✅ Fonctionne    |
| MP4          | MP3         | ✅ Fonctionne    |
| WebM         | Opus        | ✅ Fonctionne    |
| AVI          | PCM         | ✅ Fonctionne    |
| MKV          | FLAC        | ✅ Fonctionne    |

**Note**: ffmpeg gère automatiquement tous les codecs pour extraire en WAV.

---

## Test 5: Performance

### Mesures

Comparer le temps de traitement:

| Configuration | Temps Attendu | Overhead Audio |
|---------------|---------------|----------------|
| Sans lip sync | T             | -              |
| Avec lip sync | T + 5-10s     | ~5-10s         |

**Overhead audio** = temps d'extraction (1-3s) + fusion (2-7s)

---

## Checklist de Validation Complète

### Fonctionnel
- [ ] Extraction audio fonctionne (fichier WAV créé dans `temp/`)
- [ ] Commande FaceFusion inclut `--audio-path`
- [ ] Processeur `lip_syncer` ajouté quand activé
- [ ] Fusion audio fonctionne (audio dans vidéo finale)
- [ ] Lèvres synchronisées avec audio
- [ ] Audio préservé dans la vidéo finale

### Gestion d'Erreurs
- [ ] Erreur claire si vidéo sans audio + lip sync activé
- [ ] Erreur capturée si ffmpeg extraction échoue
- [ ] Erreur capturée si ffmpeg fusion échoue
- [ ] Logs affichés dans le terminal

### Performance
- [ ] Barres de progression correctes (0.25, 0.92)
- [ ] Pas de ré-encodage vidéo (utilise `-c:v copy`)
- [ ] Temps total acceptable (< 10s overhead)

### Fichiers
- [ ] Fichier audio temporaire créé dans `temp/`
- [ ] Fichier vidéo final dans `outputs/`
- [ ] Pas de fichiers temporaires qui traînent après échec

---

## Commandes de Débogage

### Vérifier l'audio extrait

```bash
# Écouter l'audio extrait
ffplay temp/video_name_audio.wav

# Infos sur l'audio
ffprobe temp/video_name_audio.wav
```

### Vérifier la vidéo finale

```bash
# Vérifier présence audio
ffprobe outputs/faceswap_xxx.mp4 2>&1 | grep "Audio"

# Devrait afficher:
# Stream #0:1: Audio: aac, 44100 Hz, mono, ...
```

### Tester extraction manuellement

```bash
cd "/Users/martinemenguy/Desktop/for facefusion"

# Créer dossier temp si nécessaire
mkdir -p temp

# Extraire audio
ffmpeg -y -i "path/to/video.mp4" -vn -ac 1 -ar 44100 temp/test_audio.wav

# Vérifier
ls -lh temp/test_audio.wav
ffplay temp/test_audio.wav
```

---

## Résolution de Problèmes

### Problème 1: ffmpeg not found

**Symptôme**: `❌ Extraction audio échouée: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution**:
```bash
# Mac
brew install ffmpeg

# Vérifier
which ffmpeg
ffmpeg -version
```

### Problème 2: Fichier audio vide (0 bytes)

**Symptôme**: `❌ Extraction audio échouée: fichier vide`

**Causes possibles**:
- Vidéo sans piste audio
- Codec audio non supporté (rare)
- Problème de permissions

**Debug**:
```bash
# Vérifier streams de la vidéo
ffprobe video.mp4 2>&1 | grep "Stream"

# Devrait afficher au moins:
# Stream #0:0: Video: ...
# Stream #0:1: Audio: ...  ← Si absent = pas d'audio
```

### Problème 3: Fusion audio échoue

**Symptôme**: `❌ Fusion audio/vidéo échouée. Consultez les logs.`

**Debug**:
```bash
# Tester fusion manuellement
ffmpeg -y \
  -i outputs/faceswap_xxx.mp4 \
  -i temp/xxx_audio.wav \
  -c:v copy \
  -c:a aac \
  -shortest \
  test_merge.mp4

# Vérifier erreur dans stderr
```

---

## Validation Finale

**Avant de considérer le feature comme complet**:

- [x] Code compile sans erreur
- [ ] Test 1 (lip sync activé) réussi
- [ ] Test 2 (lip sync désactivé) réussi
- [ ] Test 3 (vidéo sans audio) gère l'erreur correctement
- [ ] Documentation créée ([AUDIO_EXTRACTION_INTEGRATION.md](AUDIO_EXTRACTION_INTEGRATION.md))
- [ ] Aucune régression sur fonctionnalités existantes

---

**Date**: 2024-12-16
**Version**: V2 avec extraction audio automatique
**Status**: 🧪 Prêt pour test utilisateur
