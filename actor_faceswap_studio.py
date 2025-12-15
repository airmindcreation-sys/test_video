#!/usr/bin/env python3
"""
🎬 Actor Face Swap Studio
Application personnalisée pour le face swapping d'acteurs sur des vidéos
Basée sur FaceFusion - Interface simplifiée et intuitive
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple, List
import gradio as gr

# Ajouter le chemin de FaceFusion au PYTHONPATH
FACEFUSION_PATH = Path(__file__).parent / 'facefusion'
sys.path.insert(0, str(FACEFUSION_PATH))

# Import des modules FaceFusion
os.environ['OMP_NUM_THREADS'] = '1'

from facefusion import state_manager, logger
from facefusion.args import apply_args
from facefusion.execution import get_available_execution_providers
from facefusion.filesystem import is_image, is_video
from facefusion.processors.core import get_processors_modules


# Configuration des chemins
BASE_DIR = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / 'uploads'
OUTPUTS_DIR = BASE_DIR / 'outputs'
TEMP_DIR = BASE_DIR / 'temp'

# Créer les dossiers nécessaires
for directory in [UPLOADS_DIR, OUTPUTS_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)


class FaceSwapConfig:
    """Configuration des presets de qualité"""

    PRESETS = {
        'rapide': {
            'name': '⚡ Rapide',
            'description': 'Traitement rapide, qualité standard (recommandé pour les tests)',
            'face_swapper_model': 'inswapper_128',
            'face_swapper_pixel_boost': '256',
            'execution_providers': ['cpu'],
            'output_video_quality': 75,
            'face_enhancer_enabled': False
        },
        'equilibre': {
            'name': '⚖️ Équilibré',
            'description': 'Bon compromis vitesse/qualité (recommandé pour la production)',
            'face_swapper_model': 'inswapper_128',
            'face_swapper_pixel_boost': '512',
            'execution_providers': ['cuda', 'cpu'],
            'output_video_quality': 85,
            'face_enhancer_enabled': True
        },
        'haute_qualite': {
            'name': '💎 Haute Qualité',
            'description': 'Meilleure qualité possible (plus lent)',
            'face_swapper_model': 'hyperswap_1a_256',
            'face_swapper_pixel_boost': '1024',
            'execution_providers': ['cuda', 'cpu'],
            'output_video_quality': 95,
            'face_enhancer_enabled': True
        }
    }

    MODELS = {
        'inswapper_128': 'InSwapper 128 - Rapide et fiable',
        'inswapper_128_fp16': 'InSwapper 128 FP16 - Plus rapide (GPU)',
        'hyperswap_1a_256': 'HyperSwap 1A - Haute qualité',
        'hyperswap_1b_256': 'HyperSwap 1B - Très haute qualité',
        'simswap_256': 'SimSwap 256 - Bon équilibre',
        'ghost_2_256': 'GhostFace 2 - Naturel',
        'blendswap_256': 'BlendSwap - Fusion douce'
    }

    MASK_TYPES = {
        'occlusion': 'Automatique (détection des occlusions)',
        'box': 'Boîte complète (tout le visage)',
        'area': 'Zone spécifique',
        'region': 'Région personnalisée'
    }


class FaceSwapProcessor:
    """Gestionnaire du traitement de face swap"""

    def __init__(self):
        self.current_process = None

    def validate_inputs(self, source_path: str, target_path: str) -> Tuple[bool, str]:
        """Valide les fichiers d'entrée"""
        if not source_path or not os.path.exists(source_path):
            return False, "❌ Veuillez charger une photo source (portrait de l'acteur)"

        if not target_path or not os.path.exists(target_path):
            return False, "❌ Veuillez charger une vidéo cible"

        if not is_image(source_path):
            return False, "❌ Le fichier source doit être une image (JPG, PNG, etc.)"

        if not is_video(target_path):
            return False, "❌ Le fichier cible doit être une vidéo (MP4, AVI, MOV, etc.)"

        return True, "✅ Fichiers validés"

    def apply_preset(self, preset_name: str) -> dict:
        """Applique un preset de configuration"""
        return FaceSwapConfig.PRESETS.get(preset_name, FaceSwapConfig.PRESETS['equilibre'])

    def process_video(
        self,
        source_image_path: str,
        target_video_path: str,
        preset: str,
        model: str,
        pixel_boost: str,
        swap_weight: float,
        face_enhancer: bool,
        mask_types: List[str],
        mask_blur: float,
        execution_provider: str,
        progress=gr.Progress()
    ) -> Tuple[Optional[str], str]:
        """
        Traite la vidéo avec face swap

        Returns:
            Tuple[output_path, message]
        """
        try:
            # Validation
            valid, message = self.validate_inputs(source_image_path, target_video_path)
            if not valid:
                return None, message

            progress(0.1, desc="🔍 Validation des fichiers...")

            # Préparation de la sortie
            output_filename = f"faceswap_{Path(target_video_path).stem}_{preset}.mp4"
            output_path = str(OUTPUTS_DIR / output_filename)

            progress(0.2, desc="⚙️ Configuration de FaceFusion...")

            # Configuration de FaceFusion via state_manager
            config = {
                'source_paths': [source_image_path],
                'target_path': target_video_path,
                'output_path': output_path,
                'processors': ['face_swapper'],
                'face_swapper_model': model,
                'face_swapper_pixel_boost': pixel_boost,
                'face_swapper_weight': swap_weight,
                'face_mask_types': mask_types if mask_types else ['occlusion'],
                'face_mask_blur': mask_blur,
                'execution_providers': [execution_provider],
                'execution_thread_count': 4,
                'output_video_quality': 85,
                'output_video_encoder': 'libx264',
                'temp_path': str(TEMP_DIR),
                'keep_temp': False,
                'log_level': 'info'
            }

            # Ajouter face_enhancer si activé
            if face_enhancer:
                config['processors'].append('face_enhancer')
                config['face_enhancer_model'] = 'gfpgan_1.4'
                config['face_enhancer_blend'] = 80

            progress(0.3, desc="🎭 Initialisation des processeurs...")

            # Appliquer la configuration
            apply_args(config, state_manager.init_item)

            progress(0.4, desc="🚀 Lancement du traitement...")

            # Import du workflow
            from facefusion.workflows import image_to_video

            # Pré-vérifications
            if not image_to_video.pre_check():
                return None, "❌ Erreur lors de la vérification des prérequis"

            progress(0.5, desc="🎬 Traitement de la vidéo en cours...")

            # Traitement
            if not image_to_video.run():
                return None, "❌ Erreur lors du traitement de la vidéo"

            progress(0.9, desc="🎉 Finalisation...")

            # Vérifier que le fichier de sortie existe
            if not os.path.exists(output_path):
                return None, "❌ Le fichier de sortie n'a pas été créé"

            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB

            progress(1.0, desc="✅ Terminé !")

            return output_path, f"✅ Face swap terminé avec succès !\n📁 Fichier: {output_filename}\n💾 Taille: {file_size:.2f} MB"

        except Exception as e:
            error_msg = f"❌ Erreur lors du traitement: {str(e)}"
            logger.error(error_msg, __name__)
            return None, error_msg

        finally:
            # Nettoyage
            progress(1.0, desc="🧹 Nettoyage...")


# Instance globale du processeur
processor = FaceSwapProcessor()


def create_gradio_interface():
    """Crée l'interface Gradio personnalisée"""

    # Détection des providers disponibles
    available_providers = get_available_execution_providers()
    default_provider = 'cuda' if 'cuda' in available_providers else 'cpu'

    # Thème personnalisé
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter")
    )

    with gr.Blocks(
        title="🎬 Actor Face Swap Studio",
        theme=theme,
        css="""
        .main-header {
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
        }
        .preset-card {
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .info-box {
            background-color: #f0f9ff;
            border-left: 4px solid #3b82f6;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .warning-box {
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
        }
        """
    ) as app:

        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🎬 Actor Face Swap Studio</h1>
            <p>Remplacez le visage d'un acteur dans vos vidéos avec intelligence artificielle</p>
        </div>
        """)

        # Instructions principales
        gr.Markdown("""
        ### 📋 Comment utiliser cette application :

        1. **Chargez le portrait** de votre acteur (photo claire du visage)
        2. **Chargez la vidéo** où vous voulez insérer le visage
        3. **Choisissez un preset** de qualité ou ajustez manuellement les paramètres
        4. **Cliquez sur "Lancer le Face Swap"** et patientez
        5. **Téléchargez le résultat** une fois le traitement terminé
        """)

        with gr.Row():
            # Colonne gauche: Fichiers d'entrée
            with gr.Column(scale=1):
                gr.Markdown("### 📁 Étape 1: Fichiers d'entrée")

                source_image = gr.Image(
                    label="🎭 Portrait de l'acteur (Source)",
                    type="filepath",
                    sources=["upload"],
                    height=300
                )
                gr.Markdown("""
                <div class="info-box">
                ℹ️ <b>Conseils pour la photo source:</b><br>
                • Visage bien éclairé et net<br>
                • Face caméra (de préférence)<br>
                • Haute résolution recommandée<br>
                • Formats: JPG, PNG, WEBP
                </div>
                """)

                target_video = gr.Video(
                    label="🎥 Vidéo cible (où insérer le visage)",
                    sources=["upload"],
                    height=300
                )
                gr.Markdown("""
                <div class="info-box">
                ℹ️ <b>Formats vidéo supportés:</b><br>
                MP4, AVI, MOV, MKV, WEBM, etc.
                </div>
                """)

            # Colonne centrale: Paramètres
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Étape 2: Configuration")

                # Presets
                gr.Markdown("#### 🎯 Presets de qualité")
                preset_radio = gr.Radio(
                    choices=[
                        ('⚡ Rapide - Tests et aperçus', 'rapide'),
                        ('⚖️ Équilibré - Recommandé', 'equilibre'),
                        ('💎 Haute Qualité - Production', 'haute_qualite')
                    ],
                    value='equilibre',
                    label="Choisissez un preset",
                    info="Le preset ajuste automatiquement tous les paramètres"
                )

                preset_info = gr.Markdown(FaceSwapConfig.PRESETS['equilibre']['description'])

                # Paramètres avancés (repliables)
                with gr.Accordion("🔧 Paramètres avancés (optionnel)", open=False):
                    model_dropdown = gr.Dropdown(
                        choices=list(FaceSwapConfig.MODELS.items()),
                        value='inswapper_128',
                        label="Modèle de face swap",
                        info="Algorithme de remplacement de visage"
                    )

                    pixel_boost_slider = gr.Radio(
                        choices=['256', '512', '1024'],
                        value='512',
                        label="Résolution du swap (Pixel Boost)",
                        info="Plus élevé = meilleure qualité mais plus lent"
                    )

                    swap_weight = gr.Slider(
                        minimum=0.5,
                        maximum=1.0,
                        value=0.85,
                        step=0.05,
                        label="Intensité du swap",
                        info="Force de remplacement (0.5 = subtil, 1.0 = complet)"
                    )

                    face_enhancer = gr.Checkbox(
                        label="Activer l'amélioration du visage",
                        value=True,
                        info="Améliore la qualité du visage swappé (recommandé)"
                    )

                    mask_types = gr.CheckboxGroup(
                        choices=list(FaceSwapConfig.MASK_TYPES.items()),
                        value=['occlusion'],
                        label="Types de masques",
                        info="Zones à inclure dans le swap"
                    )

                    mask_blur = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.3,
                        step=0.1,
                        label="Flou du masque",
                        info="Adoucit les bords (0 = net, 1 = flou)"
                    )

                    execution_provider = gr.Dropdown(
                        choices=available_providers,
                        value=default_provider,
                        label="Provider d'exécution",
                        info="GPU (CUDA) si disponible, sinon CPU"
                    )

                # Bouton de traitement
                gr.Markdown("---")
                process_btn = gr.Button(
                    "🚀 Lancer le Face Swap",
                    variant="primary",
                    size="lg",
                    scale=1
                )

                status_text = gr.Textbox(
                    label="📊 Statut",
                    value="En attente...",
                    interactive=False,
                    lines=3
                )

            # Colonne droite: Résultat
            with gr.Column(scale=1):
                gr.Markdown("### 🎉 Étape 3: Résultat")

                output_video = gr.Video(
                    label="✨ Vidéo avec face swap",
                    height=500
                )

                gr.Markdown("""
                <div class="info-box">
                ℹ️ <b>Après le traitement:</b><br>
                • Prévisualisez directement dans le lecteur<br>
                • Cliquez sur ⋮ pour télécharger<br>
                • Les fichiers sont sauvegardés dans /outputs/
                </div>
                """)

                gr.Markdown("""
                <div class="warning-box">
                ⚠️ <b>Temps de traitement:</b><br>
                • Rapide: ~1-2 min par minute de vidéo<br>
                • Équilibré: ~3-5 min par minute<br>
                • Haute qualité: ~10-15 min par minute<br>
                (avec GPU CUDA, beaucoup plus lent sur CPU)
                </div>
                """)

        # Footer avec informations
        gr.Markdown("""
        ---
        ### 💡 Astuces pour de meilleurs résultats:

        - **Éclairage similaire**: Choisissez une photo source avec un éclairage similaire à la vidéo
        - **Angle de vue**: Pour les meilleurs résultats, l'angle du visage dans la vidéo devrait être similaire à la photo
        - **Résolution**: Utilisez des images et vidéos haute résolution
        - **Tests**: Commencez avec le preset "Rapide" sur un extrait court pour tester

        ### 🔧 Dépannage:

        - **Erreur de mémoire**: Réduisez le Pixel Boost ou utilisez un preset plus léger
        - **Visages non détectés**: Assurez-vous que les visages sont clairement visibles
        - **Résultat pas naturel**: Réduisez l'intensité du swap ou activez l'amélioration du visage

        ---
        <center>
        <small>Propulsé par <b>FaceFusion</b> | Créé pour le face swapping d'acteurs</small>
        </center>
        """)

        # Logique de mise à jour automatique des paramètres selon le preset
        def update_preset(preset_name):
            preset = FaceSwapConfig.PRESETS[preset_name]
            provider = preset['execution_providers'][0] if preset['execution_providers'][0] in available_providers else default_provider

            return [
                preset['description'],  # preset_info
                preset['face_swapper_model'],  # model
                preset['face_swapper_pixel_boost'],  # pixel_boost
                preset['face_enhancer_enabled'],  # face_enhancer
                provider  # execution_provider
            ]

        preset_radio.change(
            fn=update_preset,
            inputs=[preset_radio],
            outputs=[preset_info, model_dropdown, pixel_boost_slider, face_enhancer, execution_provider]
        )

        # Événement de traitement
        process_btn.click(
            fn=processor.process_video,
            inputs=[
                source_image,
                target_video,
                preset_radio,
                model_dropdown,
                pixel_boost_slider,
                swap_weight,
                face_enhancer,
                mask_types,
                mask_blur,
                execution_provider
            ],
            outputs=[output_video, status_text]
        )

    return app


def main():
    """Point d'entrée principal de l'application"""

    print("🎬 Actor Face Swap Studio - Démarrage...")
    print(f"📁 Dossier de sortie: {OUTPUTS_DIR}")
    print(f"🔧 Dossier temporaire: {TEMP_DIR}")

    # Initialiser le logger FaceFusion
    logger.init('info')

    # Détecter les providers disponibles
    providers = get_available_execution_providers()
    print(f"⚙️ Providers disponibles: {', '.join(providers)}")

    if 'cuda' in providers:
        print("🚀 GPU CUDA détecté - Traitement rapide disponible!")
    else:
        print("⚠️ Pas de GPU détecté - Le traitement sera sur CPU (plus lent)")

    # Créer et lancer l'interface
    app = create_gradio_interface()

    print("\n" + "="*60)
    print("✅ Interface prête !")
    print("🌐 Ouvrez votre navigateur à l'adresse indiquée ci-dessous")
    print("="*60 + "\n")

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Mettre True pour un lien public partageable
        inbrowser=True,  # Ouvre automatiquement le navigateur
        show_error=True
    )


if __name__ == "__main__":
    main()
