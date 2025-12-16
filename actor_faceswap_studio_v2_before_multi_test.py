#!/usr/bin/env python3
"""
🎬 Actor Face Swap Studio V2
Application personnalisée pour le face swapping d'acteurs sur des vidéos
Utilise FaceFusion en ligne de commande (headless mode)
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import gradio as gr
import shutil

# Configuration des chemins
BASE_DIR = Path(__file__).parent
FACEFUSION_DIR = BASE_DIR / 'facefusion'
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
            'description': 'Tests rapides - qualité standard',
            'face_swapper_model': 'inswapper_128',
            'face_swapper_pixel_boost': '256x256',
            'face_enhancer_model': 'gfpgan_1.4',
            'face_enhancer_blend': '60',
            'face_detector_size': '640x640',
            'reference_face_distance': '0.6',
            'output_video_quality': 80,
            'face_enhancer': True,
            'lip_sync': True
        },
        'equilibre': {
            'name': '⚖️ Optimal',
            'description': 'RESSEMBLANCE MAXIMALE - Configuration optimale',
            'face_swapper_model': 'inswapper_128_fp16',
            'face_swapper_pixel_boost': '512x512',
            'face_enhancer_model': 'codeformer',
            'face_enhancer_blend': '80',
            'face_detector_size': '640x640',
            'reference_face_distance': '0.6',
            'output_video_quality': 90,
            'face_enhancer': True,
            'lip_sync': True
        },
        'haute_qualite': {
            'name': '💎 Haute Qualité',
            'description': 'Qualité maximale - YouTube/Production',
            'face_swapper_model': 'inswapper_128_fp16',
            'face_swapper_pixel_boost': '1024x1024',
            'face_enhancer_model': 'codeformer',
            'face_enhancer_blend': '85',
            'face_detector_size': '640x640',
            'reference_face_distance': '0.6',
            'output_video_quality': 95,
            'face_enhancer': True,
            'lip_sync': True
        }
    }

    FACE_SWAPPER_MODELS = [
        'inswapper_128',
        'inswapper_128_fp16',
        'hyperswap_1a_256',
        'hyperswap_1b_256',
        'simswap_256',
        'ghost_2_256',
        'blendswap_256'
    ]

    LIP_SYNC_MODELS = [
        'wav2lip_gan_96',
        'wav2lip_96',
        'edtalk_256'
    ]

    FACE_ENHANCER_MODELS = [
        'codeformer',
        'gfpgan_1.4',
        'gfpgan_1.3',
        'gfpgan_1.2'
    ]

    FACE_DETECTOR_SIZES = [
        '640x640'  # Seule valeur acceptée par FaceFusion
    ]


class FaceSwapProcessor:
    """Gestionnaire du traitement de face swap via CLI"""

    def __init__(self):
        self.facefusion_script = FACEFUSION_DIR / 'facefusion.py'

    def validate_inputs(self, source_path: str, target_path: str) -> Tuple[bool, str]:
        """Valide les fichiers d'entrée"""
        if not source_path or not os.path.exists(source_path):
            return False, "❌ Veuillez charger une photo source (portrait de l'acteur)"

        if not target_path or not os.path.exists(target_path):
            return False, "❌ Veuillez charger une vidéo cible"

        if not self.facefusion_script.exists():
            return False, f"❌ FaceFusion non trouvé à {self.facefusion_script}"

        return True, "✅ Fichiers validés"

    def build_command(
        self,
        source_path: str,
        target_path: str,
        output_path: str,
        audio_path: Optional[str],
        face_swapper_model: str,
        pixel_boost: str,
        face_enhancer: bool,
        face_enhancer_model: str,
        face_enhancer_blend: str,
        face_detector_size: str,
        reference_face_distance: str,
        lip_sync_enabled: bool,
        lip_sync_model: str,
        execution_provider: str,
        output_video_quality: int
    ) -> list:
        """Construit la commande FaceFusion avec paramètres optimaux"""

        cmd = [
            'python3',
            str(self.facefusion_script),
            'headless-run',  # Mode headless pour automatisation
        ]

        # Source paths: image + audio (si lip sync activé)
        if audio_path:
            # Audio + Image dans --source-paths (ordre important)
            cmd.extend(['--source-paths', audio_path, source_path])
        else:
            # Juste l'image
            cmd.extend(['--source-paths', source_path])

        # Target et output
        cmd.extend([
            '--target-path', target_path,
            '--output-path', output_path,
        ])

        # Processeurs (l'ordre est important)
        processors = ['face_swapper']
        if face_enhancer:
            processors.append('face_enhancer')
        if lip_sync_enabled:
            processors.append('lip_syncer')

        cmd.append('--processors')
        cmd.extend(processors)

        # Face swapper options
        cmd.extend([
            '--face-swapper-model', face_swapper_model,
            '--face-swapper-pixel-boost', pixel_boost
        ])

        # Face detector options (CRITIQUE pour ressemblance)
        cmd.extend([
            '--face-detector-size', face_detector_size,
            '--face-detector-score', '0.5'
        ])

        # Reference face distance (PARAMÈTRE CLÉ pour ressemblance)
        cmd.extend([
            '--reference-face-distance', str(reference_face_distance),
            '--face-selector-mode', 'reference',
            '--face-selector-order', 'large-small'
        ])

        # Face enhancer options (avec modèle configurable)
        if face_enhancer:
            cmd.extend([
                '--face-enhancer-model', face_enhancer_model,
                '--face-enhancer-blend', str(face_enhancer_blend)
            ])

        # Lip sync options
        if lip_sync_enabled:
            cmd.extend([
                '--lip-syncer-model', lip_sync_model,
                '--lip-syncer-weight', '1.0'
            ])

        # Execution
        cmd.extend([
            '--execution-providers', execution_provider,
            '--execution-thread-count', '16'
        ])

        # Output
        cmd.extend([
            '--output-video-encoder', 'libx264',
            '--output-video-quality', str(output_video_quality)
        ])

        return cmd

    def extract_audio(self, target_video_path: str) -> Tuple[bool, Optional[str]]:
        """Extrait la piste audio en WAV pour le lip syncer"""

        audio_output = TEMP_DIR / f"{Path(target_video_path).stem}_audio.wav"

        cmd = [
            'ffmpeg', '-y',
            '-i', target_video_path,
            '-vn',
            '-ac', '1',
            '-ar', '44100',
            str(audio_output)
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as exc:
            print(f"❌ Extraction audio échouée: {exc.stderr}")
            return False, None

        if not audio_output.exists() or audio_output.stat().st_size == 0:
            print("❌ Extraction audio échouée: fichier vide")
            return False, None

        return True, str(audio_output)

    def merge_audio_into_video(self, video_path: str, audio_path: str) -> Tuple[bool, str]:
        """Relie l'audio traité à la vidéo finale pour le téléchargement"""

        merged_path = TEMP_DIR / f"{Path(video_path).stem}_with_audio.mp4"

        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            str(merged_path)
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as exc:
            print(f"❌ Fusion audio/vidéo échouée: {exc.stderr}")
            return False, video_path

        # Remplacer le fichier original par la version avec audio
        shutil.move(str(merged_path), video_path)
        return True, video_path

    def process_video(
        self,
        source_image_path: str,
        target_video_path: str,
        preset: str,
        face_swapper_model: str,
        pixel_boost: str,
        face_enhancer: bool,
        face_enhancer_model: str,
        face_enhancer_blend: str,
        face_detector_size: str,
        reference_face_distance: str,
        lip_sync_enabled: bool,
        lip_sync_model: str,
        execution_provider: str,
        output_video_quality: int,
        progress=gr.Progress()
    ) -> Tuple[Optional[str], str]:
        """
        Traite la vidéo avec face swap et paramètres optimaux

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

            # Extraction audio si lip sync activé
            audio_path: Optional[str] = None
            if lip_sync_enabled:
                progress(0.25, desc="🎵 Extraction de l'audio pour le lip sync...")
                ok, extracted_audio = self.extract_audio(target_video_path)
                if not ok or not extracted_audio:
                    return None, "❌ Échec de l'extraction audio pour le lip sync. Vérifiez que la vidéo contient une piste audio."
                audio_path = extracted_audio

            progress(0.35, desc="⚙️ Construction de la commande...")

            # Construire la commande
            cmd = self.build_command(
                source_image_path,
                target_video_path,
                output_path,
                audio_path,
                face_swapper_model,
                pixel_boost,
                face_enhancer,
                face_enhancer_model,
                face_enhancer_blend,
                face_detector_size,
                reference_face_distance,
                lip_sync_enabled,
                lip_sync_model,
                execution_provider,
                output_video_quality
            )

            print(f"\n🚀 Commande FaceFusion:")
            print(f"   {' '.join(cmd)}\n")

            progress(0.45, desc="🎬 Lancement du traitement FaceFusion...")

            # Lancer la commande
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=str(FACEFUSION_DIR)
            )

            # Lire la sortie en temps réel
            progress(0.55, desc="🎭 Traitement en cours...")
            for line in process.stdout:
                print(line.rstrip())
                # Mise à jour de la progression basée sur les logs
                if 'Processing' in line or 'Extracting' in line:
                    progress(0.65, desc="🎬 Traitement des frames...")
                elif 'Merging' in line or 'Encoding' in line:
                    progress(0.8, desc="🎥 Encodage de la vidéo...")

            # Attendre la fin
            return_code = process.wait()

            if return_code != 0:
                return None, f"❌ Erreur lors du traitement (code: {return_code})\n\nVoir les logs dans le terminal."

            progress(0.9, desc="🎉 Finalisation...")

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

            progress(1.0, desc="✅ Terminé !")

            success_msg = f"""✅ Face swap terminé avec succès !

📁 Fichier: {output_filename}
💾 Taille: {file_size:.2f} MB
📂 Dossier: {OUTPUTS_DIR}

{'🎤 Lip sync activé' if lip_sync_enabled else ''}
{'✨ Face enhancer activé' if face_enhancer else ''}
"""
            return output_path, success_msg

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"\n❌ ERREUR:\n{error_trace}\n")
            return None, f"❌ Erreur: {str(e)}\n\n⚠️ Voir les logs dans le terminal."


# Instance globale du processeur
processor = FaceSwapProcessor()


def create_gradio_interface():
    """Crée l'interface Gradio personnalisée"""

    # Détection des providers disponibles
    # Par défaut on propose cpu et cuda
    available_providers = ['cpu', 'cuda', 'coreml']
    default_provider = 'cuda'

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
        .info-box {
            background-color: #f0f9ff;
            border-left: 4px solid #3b82f6;
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
            <p style="font-size: 0.9em; opacity: 0.9;">Propulsé par FaceFusion CLI</p>
        </div>
        """)

        gr.Markdown("""
        ### 📋 Mode d'emploi :
        1. Chargez le portrait de votre acteur
        2. Chargez la vidéo
        3. Choisissez un preset ou ajustez les paramètres
        4. Cliquez sur "Lancer le Face Swap"
        """)

        with gr.Row():
            # Colonne gauche: Fichiers
            with gr.Column(scale=1):
                gr.Markdown("### 📁 Fichiers d'entrée")

                source_image = gr.Image(
                    label="🎭 Portrait de l'acteur",
                    type="filepath",
                    sources=["upload"],
                    height=250
                )

                target_video = gr.Video(
                    label="🎥 Vidéo cible",
                    sources=["upload"],
                    height=250
                )

            # Colonne centrale: Paramètres
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Configuration")

                preset_radio = gr.Radio(
                    choices=[
                        ('⚡ Rapide - Tests', 'rapide'),
                        ('⚖️ Équilibré - Recommandé', 'equilibre'),
                        ('💎 Haute Qualité - Production', 'haute_qualite')
                    ],
                    value='equilibre',
                    label="Preset de qualité"
                )

                preset_info = gr.Markdown(FaceSwapConfig.PRESETS['equilibre']['description'])

                with gr.Accordion("🔧 Paramètres avancés", open=False):
                    gr.Markdown("#### 🎭 Face Swapper")

                    face_swapper_model = gr.Dropdown(
                        choices=FaceSwapConfig.FACE_SWAPPER_MODELS,
                        value='inswapper_128_fp16',
                        label="Modèle de face swap",
                        info="inswapper_128_fp16 = meilleure ressemblance"
                    )

                    pixel_boost = gr.Radio(
                        choices=['256x256', '512x512', '1024x1024'],
                        value='512x512',
                        label="Résolution (Pixel Boost)"
                    )

                    gr.Markdown("#### ✨ Face Enhancer")

                    face_enhancer = gr.Checkbox(
                        label="✨ Activer l'amélioration du visage",
                        value=True,
                        info="OBLIGATOIRE pour ressemblance optimale"
                    )

                    face_enhancer_model = gr.Dropdown(
                        choices=FaceSwapConfig.FACE_ENHANCER_MODELS,
                        value='codeformer',
                        label="Modèle d'amélioration",
                        info="CodeFormer préserve mieux l'identité"
                    )

                    face_enhancer_blend = gr.Slider(
                        minimum=50,
                        maximum=100,
                        value=80,
                        step=5,
                        label="Intensité de l'amélioration (%)"
                    )

                    gr.Markdown("#### 🎯 Détection et Ressemblance (CRITIQUE)")

                    face_detector_size = gr.Radio(
                        choices=FaceSwapConfig.FACE_DETECTOR_SIZES,
                        value='640x640',
                        label="Taille du détecteur",
                        info="640x640 (seule valeur disponible dans FaceFusion)"
                    )

                    reference_face_distance = gr.Slider(
                        minimum=0.3,
                        maximum=1.5,
                        value=0.6,
                        step=0.1,
                        label="Distance de référence",
                        info="0.6 = optimal | < 0.6 = strict | > 0.6 = permissif"
                    )

                    gr.Markdown("#### 🎤 Lip Sync")

                    lip_sync_enabled = gr.Checkbox(
                        label="🎤 Activer la synchronisation labiale",
                        value=True,
                        info="RECOMMANDÉ si l'acteur parle"
                    )

                    lip_sync_model = gr.Dropdown(
                        choices=FaceSwapConfig.LIP_SYNC_MODELS,
                        value='wav2lip_gan_96',
                        label="Modèle de Lip Sync"
                    )

                    gr.Markdown("#### ⚙️ Exécution")

                    execution_provider = gr.Dropdown(
                        choices=available_providers,
                        value=default_provider,
                        label="Provider d'exécution",
                        info="cuda pour GPU, cpu sinon"
                    )

                    output_video_quality = gr.Slider(
                        minimum=70,
                        maximum=100,
                        value=90,
                        step=5,
                        label="Qualité vidéo de sortie (%)"
                    )

                gr.Markdown("---")
                process_btn = gr.Button(
                    "🚀 Lancer le Face Swap",
                    variant="primary",
                    size="lg"
                )

                status_text = gr.Textbox(
                    label="📊 Statut",
                    value="En attente...",
                    interactive=False,
                    lines=6
                )

            # Colonne droite: Résultat
            with gr.Column(scale=1):
                gr.Markdown("### 🎉 Résultat")

                output_video = gr.Video(
                    label="✨ Vidéo avec face swap",
                    height=500
                )

                gr.Markdown("""
                <div class="info-box">
                💡 <b>Astuce:</b> Les vidéos sont sauvegardées dans <code>outputs/</code>
                </div>
                """)

        # Footer
        gr.Markdown("""
        ---
        ### 💡 Conseils pour RESSEMBLANCE MAXIMALE:
        - **Modèle**: `inswapper_128_fp16` (meilleure fidélité d'identité)
        - **Face Enhancer**: `codeformer` à 80% (préserve les traits uniques)
        - **Distance**: 0.6 optimal | 0.3-0.5 pour strict | 0.8-1.2 pour angles difficiles
        - **Détecteur**: 1024x1024 pour vidéos HD (capture micro-expressions)
        - **Lip Sync**: Améliore le résultat de 60-80% pour dialogues
        - **Photo source**: Bien éclairée, expression neutre, haute résolution
        - Les logs détaillés s'affichent dans le terminal
        """)

        # Logique de mise à jour du preset
        def update_preset(preset_name):
            preset = FaceSwapConfig.PRESETS[preset_name]
            return [
                preset['description'],
                preset['face_swapper_model'],
                preset['face_swapper_pixel_boost'],
                preset['face_enhancer'],
                preset['face_enhancer_model'],
                preset['face_enhancer_blend'],
                preset['face_detector_size'],
                preset['reference_face_distance'],
                preset['lip_sync'],
                preset['output_video_quality']
            ]

        preset_radio.change(
            fn=update_preset,
            inputs=[preset_radio],
            outputs=[
                preset_info,
                face_swapper_model,
                pixel_boost,
                face_enhancer,
                face_enhancer_model,
                face_enhancer_blend,
                face_detector_size,
                reference_face_distance,
                lip_sync_enabled,
                output_video_quality
            ]
        )

        # Événement de traitement
        process_btn.click(
            fn=processor.process_video,
            inputs=[
                source_image,
                target_video,
                preset_radio,
                face_swapper_model,
                pixel_boost,
                face_enhancer,
                face_enhancer_model,
                face_enhancer_blend,
                face_detector_size,
                reference_face_distance,
                lip_sync_enabled,
                lip_sync_model,
                execution_provider,
                output_video_quality
            ],
            outputs=[output_video, status_text]
        )

    return app


def main():
    """Point d'entrée principal"""

    print("🎬 Actor Face Swap Studio V2 - Démarrage...")
    print(f"📁 FaceFusion: {FACEFUSION_DIR}")
    print(f"📁 Outputs: {OUTPUTS_DIR}")

    if not FACEFUSION_DIR.exists():
        print(f"❌ ERREUR: FaceFusion non trouvé à {FACEFUSION_DIR}")
        print("   Assurez-vous d'avoir installé FaceFusion dans le dossier 'facefusion'")
        return

    app = create_gradio_interface()

    print("\n" + "="*60)
    print("✅ Interface prête !")
    print("="*60 + "\n")

    # Try to use the GRADIO_SERVER_PORT environment variable, otherwise default to 7861
    import os
    port = int(os.environ.get('GRADIO_SERVER_PORT', 7861))

    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        inbrowser=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
