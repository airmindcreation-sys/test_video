# 🎵 Intégration de l'Extraction et Fusion Audio pour Lip Sync

## Vue d'ensemble

L'application extrait maintenant automatiquement l'audio de la vidéo cible pour le lip sync et le réintègre dans la vidéo finale.

## Flux Complet

```
1. User uploads vidéo + photo
2. User active lip sync
3. App extrait audio (WAV) de la vidéo
   └─> Utilise ffmpeg pour extraire en mono 44.1kHz
4. App lance FaceFusion avec --audio-path
   └─> FaceFusion synchronise les lèvres avec l'audio
5. App fusionne l'audio dans la vidéo finale
   └─> Utilise ffmpeg pour encoder l'audio en AAC
6. User télécharge la vidéo complète (vidéo + audio)
```

## Modifications Apportées

### 1. Ajout du paramètre `audio_path` dans `build_command()`

**Avant:**
```python
def build_command(
    self,
    source_path: str,
    target_path: str,
    output_path: str,
    face_swapper_model: str,
    # ... autres paramètres
) -> list:
```

**Après:**
```python
def build_command(
    self,
    source_path: str,
    target_path: str,
    output_path: str,
    audio_path: Optional[str],  # ✅ NOUVEAU
    face_swapper_model: str,
    # ... autres paramètres
) -> list:
```

**Dans le corps de la méthode:**
```python
# Ajouter le chemin audio pour le lip syncer si disponible
if audio_path:
    cmd.extend(['--audio-path', audio_path])
```

### 2. Nouvelle méthode `extract_audio()`

```python
def extract_audio(self, target_video_path: str) -> Tuple[bool, Optional[str]]:
    """Extrait la piste audio en WAV pour le lip syncer"""

    audio_output = TEMP_DIR / f"{Path(target_video_path).stem}_audio.wav"

    cmd = [
        'ffmpeg', '-y',
        '-i', target_video_path,
        '-vn',           # Pas de vidéo
        '-ac', '1',      # Mono
        '-ar', '44100',  # 44.1 kHz
        str(audio_output)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        print(f"❌ Extraction audio échouée: {exc.stderr}")
        return False, None

    if not audio_output.exists() or audio_output.stat().st_size == 0:
        print("❌ Extraction audio échouée: fichier vide")
        return False, None

    return True, str(audio_output)
```

**Pourquoi ces paramètres:**
- `-vn`: Ne traite QUE l'audio (pas la vidéo)
- `-ac 1`: Mono (lip sync ne nécessite pas stéréo)
- `-ar 44100`: Sample rate standard pour wav2lip

### 3. Nouvelle méthode `merge_audio_into_video()`

```python
def merge_audio_into_video(self, video_path: str, audio_path: str) -> Tuple[bool, str]:
    """Relie l'audio traité à la vidéo finale pour le téléchargement"""

    merged_path = TEMP_DIR / f"{Path(video_path).stem}_with_audio.mp4"

    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',    # Ne ré-encode PAS la vidéo (rapide)
        '-c:a', 'aac',     # Encode l'audio en AAC (compatible)
        '-shortest',       # Utilise la durée la plus courte
        str(merged_path)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        print(f"❌ Fusion audio/vidéo échouée: {exc.stderr}")
        return False, video_path

    # Remplacer le fichier original par la version avec audio
    shutil.move(str(merged_path), video_path)
    return True, video_path
```

**Pourquoi ces paramètres:**
- `-c:v copy`: Ne ré-encode PAS la vidéo (très rapide, pas de perte)
- `-c:a aac`: AAC est largement compatible (MP4 standard)
- `-shortest`: Évite problèmes si audio/vidéo ont durées différentes

### 4. Intégration dans `process_video()`

**Extraction avant traitement:**
```python
# Extraction audio si lip sync activé
audio_path: Optional[str] = None
if lip_sync_enabled:
    progress(0.25, desc="🎵 Extraction de l'audio pour le lip sync...")
    ok, extracted_audio = self.extract_audio(target_video_path)
    if not ok or not extracted_audio:
        return None, "❌ Échec de l'extraction audio pour le lip sync. Vérifiez que la vidéo contient une piste audio."
    audio_path = extracted_audio

progress(0.35, desc="⚙️ Construction de la commande...")

# Construire la commande AVEC audio_path
cmd = self.build_command(
    source_image_path,
    target_video_path,
    output_path,
    audio_path,  # ✅ Passé ici
    face_swapper_model,
    # ... autres paramètres
)
```

**Fusion après traitement:**
```python
# Vérifier que le fichier de sortie existe
if not os.path.exists(output_path):
    return None, "❌ Le fichier de sortie n'a pas été créé"

# Fusion audio si lip sync était activé
if lip_sync_enabled and audio_path:
    progress(0.92, desc="🔊 Fusion de l'audio final...")
    merged, output_path = self.merge_audio_into_video(output_path, audio_path)
    if not merged:
        return None, "❌ Fusion audio/vidéo échouée. Consultez les logs."

file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
```

## Barres de Progression Ajustées

```
0.1  → 🔍 Validation des fichiers
0.25 → 🎵 Extraction de l'audio (SI lip sync)
0.35 → ⚙️ Construction de la commande
0.45 → 🎬 Lancement du traitement FaceFusion
0.55 → 🎭 Traitement en cours
0.65 → 🎬 Traitement des frames
0.8  → 🎥 Encodage de la vidéo
0.9  → 🎉 Finalisation
0.92 → 🔊 Fusion de l'audio final (SI lip sync)
1.0  → ✅ Terminé!
```

## Gestion d'Erreurs

### Erreur 1: Vidéo sans piste audio
```python
if not ok or not extracted_audio:
    return None, "❌ Échec de l'extraction audio pour le lip sync. Vérifiez que la vidéo contient une piste audio."
```

### Erreur 2: Fusion échouée
```python
if not merged:
    return None, "❌ Fusion audio/vidéo échouée. Consultez les logs."
```

### Erreur 3: Fichier audio vide
```python
if not audio_output.exists() or audio_output.stat().st_size == 0:
    print("❌ Extraction audio échouée: fichier vide")
    return False, None
```

## Fichiers Temporaires

Tous les fichiers audio extraits sont stockés dans `TEMP_DIR`:
```
temp/
├── video_name_audio.wav         (audio extrait)
└── output_name_with_audio.mp4   (temporaire avant move)
```

Le fichier final remplace directement le fichier de sortie original.

## Commande FaceFusion Générée

**Sans lip sync:**
```bash
python3 facefusion.py run \
  --source-paths actor.jpg \
  --target-path video.mp4 \
  --output-path output.mp4 \
  --processors face_swapper face_enhancer \
  # ... autres paramètres
```

**Avec lip sync:**
```bash
python3 facefusion.py run \
  --source-paths actor.jpg \
  --target-path video.mp4 \
  --output-path output.mp4 \
  --audio-path temp/video_audio.wav \  # ✅ AJOUTÉ
  --processors face_swapper face_enhancer lip_syncer \
  # ... autres paramètres
```

## Avantages de cette Approche

✅ **Automatique**: User n'a rien à faire, juste cocher "Lip Sync"
✅ **Transparent**: L'audio est préservé sans intervention
✅ **Robuste**: Gestion d'erreurs à chaque étape
✅ **Rapide**: Utilise `-c:v copy` pour ne pas ré-encoder la vidéo
✅ **Compatible**: AAC audio = standard MP4

## Test du Flux

Pour tester le flux complet:

1. Lancer l'app:
   ```bash
   cd "/Users/martinemenguy/Desktop/for facefusion"
   python3 actor_faceswap_studio_v2.py
   ```

2. Upload une vidéo **avec audio**
3. Upload une photo
4. Activer "Lip Sync"
5. Lancer le traitement
6. Observer dans les logs:
   - `🎵 Extraction de l'audio pour le lip sync...`
   - `--audio-path temp/xxx_audio.wav` dans la commande
   - `🔊 Fusion de l'audio final...`

7. Télécharger et vérifier:
   - La vidéo a bien l'audio
   - Les lèvres sont synchronisées

---

**Date**: 2024-12-16
**Version**: V2 avec extraction audio automatique
**Status**: ✅ Prêt pour test
