"""
Configuration personnalisée pour Actor Face Swap Studio
Copiez ce fichier en 'config.py' et modifiez selon vos besoins
"""

# ==============================================================================
# CONFIGURATION DES PRESETS
# ==============================================================================

CUSTOM_PRESETS = {
    # Vous pouvez ajouter vos propres presets ici
    # Exemple:

    'mon_preset_ultra': {
        'name': '🚀 Ultra Performance',
        'description': 'Optimisé pour GPU très puissant, qualité maximale',
        'face_swapper_model': 'hyperswap_1b_256',
        'face_swapper_pixel_boost': '1024',
        'execution_providers': ['cuda'],
        'output_video_quality': 98,
        'face_enhancer_enabled': True
    },

    'mon_preset_leger': {
        'name': '💨 Léger',
        'description': 'Très rapide, pour aperçus rapides',
        'face_swapper_model': 'inswapper_128_fp16',
        'face_swapper_pixel_boost': '256',
        'execution_providers': ['cpu'],
        'output_video_quality': 70,
        'face_enhancer_enabled': False
    },
}

# ==============================================================================
# CONFIGURATION DES MODÈLES
# ==============================================================================

# Modèles favoris (apparaîtront en premier dans la liste)
FAVORITE_MODELS = [
    'inswapper_128',
    'hyperswap_1a_256',
    'simswap_256'
]

# ==============================================================================
# CONFIGURATION DE L'INTERFACE
# ==============================================================================

# Port de l'application (changez si 7860 est déjà utilisé)
APP_PORT = 7860

# Hôte (0.0.0.0 = accessible depuis le réseau local, 127.0.0.1 = localhost uniquement)
APP_HOST = "0.0.0.0"

# Ouvrir automatiquement le navigateur au lancement
AUTO_OPEN_BROWSER = True

# Partager publiquement via lien Gradio (True = lien public temporaire)
SHARE_PUBLIC_LINK = False

# Thème de l'interface ('soft', 'monochrome', 'glass', 'default')
GRADIO_THEME = 'soft'

# Couleur principale (pour personnaliser le thème)
PRIMARY_COLOR = 'blue'  # blue, red, green, purple, orange, etc.

# ==============================================================================
# CONFIGURATION DES CHEMINS
# ==============================================================================

# Dossiers de l'application (chemins relatifs ou absolus)
UPLOADS_FOLDER = 'uploads'
OUTPUTS_FOLDER = 'outputs'
TEMP_FOLDER = 'temp'

# Nettoyage automatique des dossiers uploads et temp après X jours
AUTO_CLEANUP_DAYS = 7  # 0 = désactivé

# ==============================================================================
# CONFIGURATION DU TRAITEMENT
# ==============================================================================

# Provider par défaut (auto-détection si None)
DEFAULT_EXECUTION_PROVIDER = None  # 'cuda', 'cpu', 'coreml', etc.

# Nombre de threads pour le traitement CPU
DEFAULT_THREAD_COUNT = 4

# Limite de mémoire système (en GB, 0 = pas de limite)
SYSTEM_MEMORY_LIMIT = 0

# Stratégie de gestion de la mémoire vidéo ('strict', 'moderate', 'relaxed')
VIDEO_MEMORY_STRATEGY = 'moderate'

# ==============================================================================
# CONFIGURATION VIDÉO
# ==============================================================================

# Encodeur vidéo par défaut
DEFAULT_VIDEO_ENCODER = 'libx264'  # libx264, libx265, libvpx-vp9, etc.

# Preset d'encodage ('ultrafast', 'fast', 'medium', 'slow', 'veryslow')
DEFAULT_VIDEO_PRESET = 'medium'

# Qualité vidéo par défaut (0-100, ou CRF 0-51 pour H.264/H.265)
DEFAULT_VIDEO_QUALITY = 85

# FPS de sortie (0 = même que la source)
DEFAULT_OUTPUT_FPS = 0

# ==============================================================================
# CONFIGURATION AUDIO
# ==============================================================================

# Encodeur audio par défaut
DEFAULT_AUDIO_ENCODER = 'aac'  # aac, mp3, opus, flac

# Qualité audio (0-100)
DEFAULT_AUDIO_QUALITY = 90

# Volume audio (0-200, 100 = identique)
DEFAULT_AUDIO_VOLUME = 100

# ==============================================================================
# CONFIGURATION DÉTECTION DE VISAGES
# ==============================================================================

# Modèle de détection par défaut
DEFAULT_FACE_DETECTOR = 'yolo_face'  # yolo_face, retinaface, scrfd, yunet, many

# Taille de détection ('320x320', '640x640', '1280x1280')
DEFAULT_FACE_DETECTOR_SIZE = '640x640'

# Score minimum de détection (0.0-1.0)
DEFAULT_FACE_DETECTOR_SCORE = 0.5

# Angles de détection (0, 90, 180, 270)
DEFAULT_FACE_DETECTOR_ANGLES = [0]

# ==============================================================================
# CONFIGURATION MASQUES
# ==============================================================================

# Types de masques par défaut
DEFAULT_MASK_TYPES = ['occlusion']  # box, occlusion, area, region

# Flou du masque (0.0-1.0)
DEFAULT_MASK_BLUR = 0.3

# Padding du masque (en pixels)
DEFAULT_MASK_PADDING = [0, 0, 0, 0]  # top, right, bottom, left

# ==============================================================================
# CONFIGURATION LOGS
# ==============================================================================

# Niveau de log ('error', 'warn', 'info', 'debug')
LOG_LEVEL = 'info'

# Sauvegarder les logs dans un fichier
SAVE_LOGS_TO_FILE = False

# Fichier de log
LOG_FILE_PATH = 'actor_faceswap_studio.log'

# ==============================================================================
# CONFIGURATION AVANCÉE
# ==============================================================================

# Garder les fichiers temporaires après traitement (utile pour debug)
KEEP_TEMP_FILES = False

# Format des frames temporaires ('jpg', 'png')
TEMP_FRAME_FORMAT = 'jpg'

# Arrêter sur erreur ou continuer
HALT_ON_ERROR = False

# Limite de taille de fichier upload (en MB, 0 = pas de limite)
MAX_UPLOAD_SIZE_MB = 0

# ==============================================================================
# MESSAGES PERSONNALISÉS
# ==============================================================================

# Titre de l'application
APP_TITLE = "🎬 Actor Face Swap Studio"

# Sous-titre
APP_SUBTITLE = "Remplacez le visage d'un acteur dans vos vidéos avec intelligence artificielle"

# Message de bienvenue (HTML supporté)
WELCOME_MESSAGE = """
### 📋 Comment utiliser cette application :

1. **Chargez le portrait** de votre acteur (photo claire du visage)
2. **Chargez la vidéo** où vous voulez insérer le visage
3. **Choisissez un preset** de qualité ou ajustez manuellement les paramètres
4. **Cliquez sur "Lancer le Face Swap"** et patientez
5. **Téléchargez le résultat** une fois le traitement terminé
"""

# Message de pied de page
FOOTER_MESSAGE = """
---
<center>
<small>Propulsé par <b>FaceFusion</b> | Créé pour le face swapping d'acteurs</small>
</center>
"""

# ==============================================================================
# EXEMPLE D'UTILISATION
# ==============================================================================

"""
Pour utiliser cette configuration personnalisée:

1. Copiez ce fichier en 'config.py'
2. Modifiez les valeurs selon vos besoins
3. Dans actor_faceswap_studio.py, importez:

   try:
       from config import *
   except ImportError:
       pass  # Utiliser les valeurs par défaut

4. Utilisez les variables de configuration dans votre code:

   app.launch(
       server_port=APP_PORT,
       server_name=APP_HOST,
       share=SHARE_PUBLIC_LINK
   )
"""

# ==============================================================================
# NOTES
# ==============================================================================

"""
NOTES IMPORTANTES:

1. PRESETS PERSONNALISÉS:
   - Les presets doivent contenir toutes les clés requises
   - Référez-vous aux presets par défaut dans actor_faceswap_studio.py

2. PROVIDERS D'EXÉCUTION:
   - cuda: GPU NVIDIA (le plus rapide)
   - cpu: CPU uniquement (lent mais compatible partout)
   - coreml: Apple Silicon (M1/M2/M3)
   - tensorrt: NVIDIA avec TensorRT (très rapide)

3. MODÈLES DISPONIBLES:
   - Consultez FaceSwapConfig.MODELS dans actor_faceswap_studio.py
   - Les modèles sont téléchargés automatiquement à la première utilisation

4. PERFORMANCE:
   - Augmentez DEFAULT_THREAD_COUNT si vous avez un CPU puissant
   - Utilisez VIDEO_MEMORY_STRATEGY='strict' si vous manquez de VRAM
   - Réduisez DEFAULT_VIDEO_QUALITY si les fichiers sont trop gros

5. SÉCURITÉ:
   - Ne mettez APP_HOST='0.0.0.0' que sur un réseau de confiance
   - Utilisez SHARE_PUBLIC_LINK avec précaution (lien public temporaire)
   - Limitez MAX_UPLOAD_SIZE_MB pour éviter les abus
"""
