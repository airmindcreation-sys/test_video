#!/usr/bin/env python3
"""
🎬 Actor Face Swap Studio V3
Application complète avec test multi-configurations et comparaison
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List, Dict
import gradio as gr
import shutil
import json
from datetime import datetime

# Configuration des chemins
BASE_DIR = Path(__file__).parent
FACEFUSION_DIR = BASE_DIR / 'facefusion'
UPLOADS_DIR = BASE_DIR / 'uploads'
OUTPUTS_DIR = BASE_DIR / 'outputs'
TEMP_DIR = BASE_DIR / 'temp'
BATCH_RESULTS_DIR = BASE_DIR / 'batch_results'

# Créer les dossiers nécessaires
for directory in [UPLOADS_DIR, OUTPUTS_DIR, TEMP_DIR, BATCH_RESULTS_DIR]:
    directory.mkdir(exist_ok=True)


class FaceSwapConfig:
    """Configuration complète avec tous les paramètres FaceFusion"""

    # Tous les modèles de face swapper
    FACE_SWAPPER_MODELS = [
        'blendswap_256',
        'ghost_1_256',
        'ghost_2_256',
        'ghost_3_256',
        'hififace_unofficial_256',
        'hyperswap_1a_256',
        'hyperswap_1b_256',
        'hyperswap_1c_256',
        'inswapper_128',
        'inswapper_128_fp16',
        'simswap_256',
        'simswap_unofficial_512',
        'uniface_256'
    ]

    # Tous les modèles de face enhancer
    FACE_ENHANCER_MODELS = [
        'clear_reality_x4',
        'lsdir_x4',
        'nomos8k_sc_x4',
        'real_esrgan_x2',
        'real_esrgan_x2_fp16',
        'real_esrgan_x4',
        'real_esrgan_x4_fp16',
        'real_esrgan_x8',
        'real_esrgan_x8_fp16',
        'real_hatgan_x4',
        'span_kendata_x4',
        'codeformer',
        'gfpgan_1.2',
        'gfpgan_1.3',
        'gfpgan_1.4'
    ]

    # Tous les modèles de frame enhancer
    FRAME_ENHANCER_MODELS = [
        'clear_reality_x4',
        'lsdir_x4',
        'nomos8k_sc_x4',
        'real_esrgan_x2',
        'real_esrgan_x2_fp16',
        'real_esrgan_x4',
        'real_esrgan_x4_fp16',
        'real_esrgan_x8',
        'real_esrgan_x8_fp16',
        'real_hatgan_x4',
        'real_web_photo_x4',
        'realistic_rescaler_x4',
        'remacri_x4',
        'siax_x4',
        'span_kendata_x4',
        'swin2_sr_x4',
        'ultra_sharp_x4',
        'ultra_sharp_2_x4'
    ]

    LIP_SYNC_MODELS = [
        'wav2lip_gan_96',
        'wav2lip_96',
        'edtalk_256'
    ]

    FACE_DETECTOR_SIZES = ['640x640']

    PIXEL_BOOST_OPTIONS = ['256x256', '512x512', '768x768', '1024x1024']

    EXECUTION_PROVIDERS = ['cpu', 'cuda', 'coreml']

    # Configurations pré-définies pour tests en groupe
    PREDEFINED_CONFIGS = {
        "golden_standard": {
            "name": "01_Golden Standard - InSwapper + CodeFormer",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "inswapper_128_fp16",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 80,
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        },
        "hyperswap_high_res": {
            "name": "02_HyperSwap 1B - Haute Résolution",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "hyperswap_1b_256",
            "face_swapper_pixel_boost": "1024x1024",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 85,
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        },
        "cinematic_gfpgan": {
            "name": "03_Cinématique - InSwapper + GFPGAN",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "inswapper_128_fp16",
            "face_enhancer_model": "gfpgan_1.4",
            "face_enhancer_blend": 75,
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        },
        "hyperswap_gfpgan": {
            "name": "04_HyperSwap + GFPGAN - Équilibré",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "hyperswap_1b_256",
            "face_enhancer_model": "gfpgan_1.4",
            "face_enhancer_blend": 70,
            "reference_face_distance": 0.7,
            "output_video_quality": 95
        },
        "strict_matching": {
            "name": "05_Matching Strict - Distance 0.4",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "inswapper_128_fp16",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 80,
            "reference_face_distance": 0.4,
            "output_video_quality": 95
        },
        "flexible_matching": {
            "name": "06_Matching Souple - Distance 0.9",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "hyperswap_1b_256",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 85,
            "reference_face_distance": 0.9,
            "output_video_quality": 95
        },
        "pixel_boost": {
            "name": "07_InSwapper - Pixel Boost 512x512",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "inswapper_128_fp16",
            "face_swapper_pixel_boost": "512x512",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 85,
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        },
        "full_pipeline": {
            "name": "08_Pipeline Complet - Frame Enhancer",
            "processors": ["face_swapper", "face_enhancer", "frame_enhancer"],
            "face_swapper_model": "hyperswap_1b_256",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 80,
            "frame_enhancer_model": "real_esrgan_x2_fp16",
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        },
        "high_blend": {
            "name": "09_Blend Élevé 90 - Naturel",
            "processors": ["face_swapper", "face_enhancer"],
            "face_swapper_model": "inswapper_128_fp16",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 90,
            "reference_face_distance": 0.5,
            "output_video_quality": 95
        },
        "fast_preview": {
            "name": "10_Preview Rapide - Sans Enhancer",
            "processors": ["face_swapper"],
            "face_swapper_model": "hyperswap_1b_256",
            "reference_face_distance": 0.6,
            "output_video_quality": 80
        },
        "with_lip_sync": {
            "name": "11_Avec Lip Sync - InSwapper + CodeFormer",
            "processors": ["face_swapper", "face_enhancer", "lip_syncer"],
            "face_swapper_model": "inswapper_128_fp16",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 80,
            "lip_syncer_model": "wav2lip_gan_96",
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        },
        "lip_sync_hyperswap": {
            "name": "12_Lip Sync + HyperSwap - Haute Qualité",
            "processors": ["face_swapper", "face_enhancer", "lip_syncer"],
            "face_swapper_model": "hyperswap_1b_256",
            "face_swapper_pixel_boost": "1024x1024",
            "face_enhancer_model": "codeformer",
            "face_enhancer_blend": 85,
            "lip_syncer_model": "wav2lip_gan_96",
            "reference_face_distance": 0.6,
            "output_video_quality": 95
        }
    }


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
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            print(f"❌ Extraction audio échouée: {exc.stderr}")
            return False, None

        if not audio_output.exists() or audio_output.stat().st_size == 0:
            return False, None

        return True, str(audio_output)

    def merge_audio_into_video(self, video_path: str, audio_path: str) -> Tuple[bool, str]:
        """Fusionne l'audio dans la vidéo finale"""
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
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            print(f"❌ Fusion audio/vidéo échouée: {exc.stderr}")
            return False, video_path

        shutil.move(str(merged_path), video_path)
        return True, video_path

    def build_command(self, config: Dict, source_path: str, target_path: str,
                     output_path: str, audio_path: Optional[str] = None) -> list:
        """Construit la commande FaceFusion à partir d'une configuration"""

        cmd = ['python3', str(self.facefusion_script), 'headless-run']

        # Source paths
        if audio_path:
            cmd.extend(['--source-paths', audio_path, source_path])
        else:
            cmd.extend(['--source-paths', source_path])

        # Target et output
        cmd.extend(['--target-path', target_path, '--output-path', output_path])

        # Processors
        processors = config.get('processors', ['face_swapper'])
        cmd.append('--processors')
        cmd.extend(processors)

        # Face swapper
        if 'face_swapper_model' in config:
            cmd.extend(['--face-swapper-model', config['face_swapper_model']])

        if 'face_swapper_pixel_boost' in config:
            cmd.extend(['--face-swapper-pixel-boost', config['face_swapper_pixel_boost']])

        # Face detector
        cmd.extend(['--face-detector-size', config.get('face_detector_size', '640x640')])
        cmd.extend(['--face-detector-score', '0.5'])

        # Reference face
        cmd.extend([
            '--reference-face-distance', str(config.get('reference_face_distance', 0.6)),
            '--face-selector-mode', 'reference',
            '--face-selector-order', 'large-small'
        ])

        # Face enhancer
        if 'face_enhancer' in processors or 'face_enhancer_model' in config:
            cmd.extend(['--face-enhancer-model', config.get('face_enhancer_model', 'codeformer')])
            cmd.extend(['--face-enhancer-blend', str(config.get('face_enhancer_blend', 80))])

        # Frame enhancer
        if 'frame_enhancer' in processors and 'frame_enhancer_model' in config:
            cmd.extend(['--frame-enhancer-model', config['frame_enhancer_model']])
            if 'frame_enhancer_blend' in config:
                cmd.extend(['--frame-enhancer-blend', str(config['frame_enhancer_blend'])])

        # Lip sync
        if 'lip_syncer' in processors:
            cmd.extend(['--lip-syncer-model', config.get('lip_syncer_model', 'wav2lip_gan_96')])
            cmd.extend(['--lip-syncer-weight', '1.0'])

        # Execution
        cmd.extend([
            '--execution-providers', config.get('execution_provider', 'cpu'),
            '--execution-thread-count', '16'
        ])

        # Output
        cmd.extend([
            '--output-video-encoder', 'libx264',
            '--output-video-quality', str(config.get('output_video_quality', 90))
        ])

        return cmd

    def run_batch_tests(self, source_image: str, target_video: str,
                       selected_configs: List[str], progress=gr.Progress()) -> Tuple[str, List, str]:
        """Execute plusieurs configurations et retourne les résultats"""

        valid, message = self.validate_inputs(source_image, target_video)
        if not valid:
            return message, [], ""

        # Créer dossier de session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = BATCH_RESULTS_DIR / f"batch_{timestamp}"
        session_dir.mkdir(exist_ok=True)

        results = []
        video_paths = []
        total = len(selected_configs)

        for i, config_key in enumerate(selected_configs):
            config = FaceSwapConfig.PREDEFINED_CONFIGS[config_key].copy()
            config_name = config.pop('name')

            progress((i / total), desc=f"⚙️ Config {i+1}/{total}: {config_name[:40]}")

            # Extraction audio si lip sync
            audio_path = None
            if 'lip_syncer' in config.get('processors', []):
                ok, audio_path = self.extract_audio(target_video)
                if not ok:
                    results.append({
                        'config': config_name,
                        'status': 'failed',
                        'error': 'Audio extraction failed'
                    })
                    continue

            # Output path
            safe_name = config_key.replace('_', '-')
            output_path = str(session_dir / f"{safe_name}.mp4")

            # Build et run command
            cmd = self.build_command(config, source_image, target_video, output_path, audio_path)

            print(f"\n🚀 Configuration {i+1}/{total}: {config_name}")
            print(f"   Command: {' '.join(cmd[:10])}...")

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(FACEFUSION_DIR))

                if result.returncode == 0 and os.path.exists(output_path):
                    # Fusion audio si nécessaire
                    if audio_path:
                        self.merge_audio_into_video(output_path, audio_path)

                    file_size = os.path.getsize(output_path) / (1024 * 1024)
                    results.append({
                        'config': config_name,
                        'status': 'success',
                        'path': output_path,
                        'size_mb': f"{file_size:.2f}"
                    })
                    video_paths.append((output_path, config_name))
                else:
                    results.append({
                        'config': config_name,
                        'status': 'failed',
                        'error': result.stderr[:200] if result.stderr else 'Unknown error'
                    })
            except Exception as e:
                results.append({
                    'config': config_name,
                    'status': 'failed',
                    'error': str(e)
                })

        # Sauvegarder résultats
        results_file = session_dir / 'results.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        # Créer résumé
        success_count = sum(1 for r in results if r['status'] == 'success')
        summary = f"""✅ Test en Groupe Terminé !

📊 Résultats: {success_count}/{total} configurations réussies
📂 Dossier: {session_dir}
📄 Détails: {results_file}

{chr(10).join([f"{'✅' if r['status'] == 'success' else '❌'} {r['config']}" for r in results])}
"""

        progress(1.0, desc="✅ Tests terminés!")

        return summary, video_paths, str(session_dir)

    def process_video_simple(self, source_image: str, target_video: str,
                            face_swapper_model: str, pixel_boost: str,
                            face_enhancer_enabled: bool, face_enhancer_model: str, face_enhancer_blend: float,
                            frame_enhancer_enabled: bool, frame_enhancer_model: str,
                            lip_sync_enabled: bool, lip_sync_model: str,
                            reference_distance: float, execution_provider: str, quality: int,
                            progress=gr.Progress()) -> Tuple[Optional[str], str, Optional[str]]:
        """Traite une vidéo avec les paramètres simples"""

        valid, message = self.validate_inputs(source_image, target_video)
        if not valid:
            return None, message, None

        progress(0.1, desc="🔍 Validation...")

        # Output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"faceswap_{Path(target_video).stem}_{timestamp}.mp4"
        output_path = str(OUTPUTS_DIR / output_filename)

        # Build config
        processors = ['face_swapper']
        if face_enhancer_enabled:
            processors.append('face_enhancer')
        if frame_enhancer_enabled:
            processors.append('frame_enhancer')
        if lip_sync_enabled:
            processors.append('lip_syncer')

        config = {
            'processors': processors,
            'face_swapper_model': face_swapper_model,
            'face_swapper_pixel_boost': pixel_boost,
            'reference_face_distance': reference_distance,
            'output_video_quality': quality,
            'execution_provider': execution_provider
        }

        if face_enhancer_enabled:
            config['face_enhancer_model'] = face_enhancer_model
            config['face_enhancer_blend'] = int(face_enhancer_blend)

        if frame_enhancer_enabled:
            config['frame_enhancer_model'] = frame_enhancer_model

        if lip_sync_enabled:
            config['lip_syncer_model'] = lip_sync_model

        # Extraction audio si lip sync
        audio_path = None
        if lip_sync_enabled:
            progress(0.25, desc="🎵 Extraction audio...")
            ok, audio_path = self.extract_audio(target_video)
            if not ok:
                return None, "❌ Échec extraction audio. Vérifiez que la vidéo contient de l'audio.", None

        progress(0.35, desc="⚙️ Construction commande...")

        # Build command
        cmd = self.build_command(config, source_image, target_video, output_path, audio_path)

        print(f"\n🚀 Commande FaceFusion:")
        print(f"   {' '.join(cmd[:15])}...\n")

        progress(0.45, desc="🎬 Traitement FaceFusion...")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(FACEFUSION_DIR))

            if result.returncode == 0 and os.path.exists(output_path):
                # Fusion audio si nécessaire
                if audio_path:
                    progress(0.92, desc="🔊 Fusion audio...")
                    self.merge_audio_into_video(output_path, audio_path)

                file_size = os.path.getsize(output_path) / (1024 * 1024)

                progress(1.0, desc="✅ Terminé!")

                success_msg = f"""✅ Face Swap Terminé !

📁 Fichier: {output_filename}
💾 Taille: {file_size:.2f} MB
📂 Dossier: {OUTPUTS_DIR}

{'🎤 Lip Sync activé' if lip_sync_enabled else ''}
{'✨ Face Enhancer activé' if face_enhancer_enabled else ''}
{'🖼️ Frame Enhancer activé' if frame_enhancer_enabled else ''}
"""
                return output_path, success_msg, output_path
            else:
                error_msg = result.stderr[:500] if result.stderr else "Erreur inconnue"
                return None, f"❌ Erreur lors du traitement:\n{error_msg}", None

        except Exception as e:
            return None, f"❌ Exception: {str(e)}", None

    def run_custom_batch_tests(self, source_image: str, target_video: str,
                               custom_configs_data: List[Dict], progress=gr.Progress()) -> Tuple[str, List, str]:
        """Execute des configurations personnalisées"""

        valid, message = self.validate_inputs(source_image, target_video)
        if not valid:
            return message, [], ""

        # Filtrer les configs activées
        enabled_configs = [c for c in custom_configs_data if c['enabled']]
        if not enabled_configs:
            return "❌ Aucune configuration activée !", [], ""

        # Créer dossier de session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = BATCH_RESULTS_DIR / f"custom_batch_{timestamp}"
        session_dir.mkdir(exist_ok=True)

        results = []
        video_paths = []
        total = len(enabled_configs)

        for i, cfg in enumerate(enabled_configs):
            config_name = cfg['name']
            progress((i / total), desc=f"⚙️ Config {i+1}/{total}: {config_name}")

            # Build config dict
            processors = ['face_swapper']
            if cfg['use_face_enh']:
                processors.append('face_enhancer')
            if cfg['use_frame_enh']:
                processors.append('frame_enhancer')
            if cfg['use_lip_sync']:
                processors.append('lip_syncer')

            config_dict = {
                'processors': processors,
                'face_swapper_model': cfg['face_swapper'],
                'face_swapper_pixel_boost': cfg['pixel_boost'],
                'reference_face_distance': cfg['distance'],
                'output_video_quality': cfg['quality'],
                'execution_provider': cfg['exec_provider']
            }

            if cfg['use_face_enh']:
                config_dict['face_enhancer_model'] = cfg['face_enh_model']
                config_dict['face_enhancer_blend'] = cfg['face_enh_blend']

            if cfg['use_frame_enh']:
                config_dict['frame_enhancer_model'] = cfg['frame_enh_model']

            if cfg['use_lip_sync']:
                config_dict['lip_syncer_model'] = cfg['lip_sync_model']

            # Extraction audio si lip sync
            audio_path = None
            if cfg['use_lip_sync']:
                ok, audio_path = self.extract_audio(target_video)
                if not ok:
                    results.append({'config': config_name, 'status': 'failed', 'error': 'Audio extraction failed'})
                    continue

            # Output path
            safe_name = config_name.replace(' ', '_').replace('/', '-')
            output_path = str(session_dir / f"{safe_name}.mp4")

            # Build et run command
            cmd = self.build_command(config_dict, source_image, target_video, output_path, audio_path)

            print(f"\n🚀 Configuration {i+1}/{total}: {config_name}")

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(FACEFUSION_DIR))

                if result.returncode == 0 and os.path.exists(output_path):
                    # Fusion audio si nécessaire
                    if audio_path:
                        self.merge_audio_into_video(output_path, audio_path)

                    file_size = os.path.getsize(output_path) / (1024 * 1024)
                    results.append({
                        'config': config_name,
                        'status': 'success',
                        'path': output_path,
                        'size_mb': f"{file_size:.2f}"
                    })
                    video_paths.append((output_path, config_name))
                else:
                    results.append({
                        'config': config_name,
                        'status': 'failed',
                        'error': result.stderr[:200] if result.stderr else 'Unknown error'
                    })
            except Exception as e:
                results.append({'config': config_name, 'status': 'failed', 'error': str(e)})

        # Sauvegarder résultats
        results_file = session_dir / 'results.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        # Créer résumé
        success_count = sum(1 for r in results if r['status'] == 'success')
        summary = f"""✅ Tests Personnalisés Terminés !

📊 Résultats: {success_count}/{total} configurations réussies
📂 Dossier: {session_dir}

{chr(10).join([f"{'✅' if r['status'] == 'success' else '❌'} {r['config']}" for r in results])}
"""

        progress(1.0, desc="✅ Tests terminés!")

        return summary, video_paths, str(session_dir)


# Instance globale
processor = FaceSwapProcessor()


def create_gradio_interface():
    """Crée l'interface Gradio complète"""

    with gr.Blocks(title="🎬 Actor Face Swap Studio V3", theme=gr.themes.Soft()) as app:

        gr.Markdown("""
        # 🎬 Actor Face Swap Studio V3
        ### Application complète avec test multi-configurations
        """)

        with gr.Tabs():

            # ==================== ONGLET 1: FACE SWAP SIMPLE ====================
            with gr.Tab("🎬 Face Swap Simple"):
                gr.Markdown("### Mode d'emploi : Upload photo + vidéo, ajuste paramètres, lance !")

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📁 Fichiers")
                        simple_source = gr.Image(label="🎭 Portrait", type="filepath", sources=["upload"])
                        simple_target = gr.Video(label="🎥 Vidéo", sources=["upload"])

                    with gr.Column(scale=1):
                        gr.Markdown("### ⚙️ Configuration")

                        # Face Swapper
                        simple_face_swapper = gr.Dropdown(
                            choices=FaceSwapConfig.FACE_SWAPPER_MODELS,
                            value='inswapper_128_fp16',
                            label="Face Swapper Model"
                        )
                        simple_pixel_boost = gr.Radio(
                            choices=FaceSwapConfig.PIXEL_BOOST_OPTIONS,
                            value='512x512',
                            label="Pixel Boost"
                        )

                        # Face Enhancer
                        simple_face_enhancer_enable = gr.Checkbox(label="Activer Face Enhancer", value=True)
                        simple_face_enhancer = gr.Dropdown(
                            choices=FaceSwapConfig.FACE_ENHANCER_MODELS,
                            value='codeformer',
                            label="Face Enhancer Model"
                        )
                        simple_face_enhancer_blend = gr.Slider(0, 100, value=80, label="Face Enhancer Blend")

                        # Frame Enhancer
                        simple_frame_enhancer_enable = gr.Checkbox(label="Activer Frame Enhancer", value=False)
                        simple_frame_enhancer = gr.Dropdown(
                            choices=FaceSwapConfig.FRAME_ENHANCER_MODELS,
                            value='real_esrgan_x2_fp16',
                            label="Frame Enhancer Model"
                        )

                        # Lip Sync
                        simple_lip_sync_enable = gr.Checkbox(label="Activer Lip Sync", value=False)
                        simple_lip_sync_model = gr.Dropdown(
                            choices=FaceSwapConfig.LIP_SYNC_MODELS,
                            value='wav2lip_gan_96',
                            label="Lip Sync Model"
                        )

                        # Autres
                        simple_reference_distance = gr.Slider(0.0, 1.0, value=0.6, step=0.05, label="Reference Face Distance")
                        simple_execution_provider = gr.Radio(
                            choices=FaceSwapConfig.EXECUTION_PROVIDERS,
                            value='cpu',
                            label="Execution Provider"
                        )
                        simple_quality = gr.Slider(0, 100, value=90, label="Output Quality")

                simple_btn = gr.Button("🚀 Lancer Face Swap", variant="primary", size="lg")

                with gr.Row():
                    simple_output_video = gr.Video(label="📹 Résultat", height=300)
                    simple_output_msg = gr.Textbox(label="Status", lines=10)

                simple_download_btn = gr.File(label="💾 Télécharger la vidéo", interactive=False)

            # ==================== ONGLET 2: TEST EN GROUPE ====================
            with gr.Tab("🧪 Test en Groupe"):
                gr.Markdown("""
                ### 🧪 Test Multi-Configurations
                Compare plusieurs configurations sur la même vidéo
                """)

                # Fichiers communs
                with gr.Row():
                    batch_source = gr.Image(label="🎭 Portrait", type="filepath", sources=["upload"])
                    batch_target = gr.Video(label="🎥 Vidéo", sources=["upload"])

                # Sous-onglets pour configs pré-définies vs personnalisées
                with gr.Tabs():
                    # ========== Configs Pré-définies ==========
                    with gr.Tab("📋 Configs Pré-définies"):
                        with gr.Row():
                            with gr.Column(scale=1):
                                gr.Markdown("### 📋 Sélection des Configurations")
                                batch_predefined_configs = gr.CheckboxGroup(
                                    choices=[(v['name'], k) for k, v in FaceSwapConfig.PREDEFINED_CONFIGS.items()],
                                    label="Configurations à tester",
                                    value=list(FaceSwapConfig.PREDEFINED_CONFIGS.keys())[:3]
                                )
                                batch_predefined_btn = gr.Button("🚀 Lancer Tests Pré-définis", variant="primary", size="lg")

                            with gr.Column(scale=2):
                                gr.Markdown("### 📊 Résultats")
                                batch_predefined_summary = gr.Textbox(label="Résumé", lines=8)
                                batch_predefined_gallery = gr.Gallery(label="📹 Vidéos", columns=3, height=400)
                                batch_predefined_player = gr.Video(label="🎬 Lecteur", interactive=False, height=300)
                                batch_predefined_path = gr.Textbox(label="📂 Dossier", interactive=False)

                    # ========== Configs Personnalisées ==========
                    with gr.Tab("⚙️ Configs Personnalisées"):
                        gr.Markdown("""
                        ### ⚙️ Créer vos propres configurations
                        Créez jusqu'à 15 configurations personnalisées
                        """)

                        # Sélecteur de nombre de configs
                        with gr.Row():
                            num_configs_slider = gr.Slider(
                                minimum=1,
                                maximum=15,
                                step=1,
                                value=3,
                                label="Nombre de configurations à créer",
                                info="Ajustez pour afficher plus ou moins de configurations"
                            )
                            update_configs_btn = gr.Button("🔄 Mettre à jour", size="sm")

                        custom_configs_list = []

                        # Créer 15 configurations (masquées par défaut)
                        for i in range(15):
                            with gr.Accordion(f"Configuration {i+1}", open=(i == 0), visible=(i < 3)) as accordion:
                                with gr.Row():
                                    cc_enabled = gr.Checkbox(label=f"Activer Config {i+1}", value=(i < 2))

                                with gr.Row():
                                    with gr.Column():
                                        cc_name = gr.Textbox(label="Nom", value=f"custom_{i+1}")
                                        cc_face_swapper = gr.Dropdown(
                                            choices=FaceSwapConfig.FACE_SWAPPER_MODELS,
                                            value='inswapper_128_fp16',
                                            label="Face Swapper"
                                        )
                                        cc_pixel_boost = gr.Dropdown(
                                            choices=FaceSwapConfig.PIXEL_BOOST_OPTIONS,
                                            value='512x512',
                                            label="Pixel Boost"
                                        )
                                        cc_use_face_enh = gr.Checkbox(label="Face Enhancer", value=True)
                                        cc_face_enh_model = gr.Dropdown(
                                            choices=FaceSwapConfig.FACE_ENHANCER_MODELS,
                                            value='codeformer',
                                            label="Face Enh. Model"
                                        )

                                    with gr.Column():
                                        cc_face_enh_blend = gr.Slider(0, 100, value=80, label="Face Enh. Blend")
                                        cc_use_frame_enh = gr.Checkbox(label="Frame Enhancer", value=False)
                                        cc_frame_enh_model = gr.Dropdown(
                                            choices=FaceSwapConfig.FRAME_ENHANCER_MODELS,
                                            value='real_esrgan_x2_fp16',
                                            label="Frame Enh. Model"
                                        )
                                        cc_use_lip_sync = gr.Checkbox(label="Lip Sync", value=False)
                                        cc_lip_sync_model = gr.Dropdown(
                                            choices=FaceSwapConfig.LIP_SYNC_MODELS,
                                            value='wav2lip_gan_96',
                                            label="Lip Sync Model"
                                        )

                                    with gr.Column():
                                        cc_distance = gr.Slider(0.0, 1.0, value=0.6, step=0.05, label="Ref. Distance")
                                        cc_quality = gr.Slider(0, 100, value=90, label="Quality")
                                        cc_exec_provider = gr.Radio(
                                            choices=FaceSwapConfig.EXECUTION_PROVIDERS,
                                            value='cpu',
                                            label="Execution"
                                        )

                                custom_configs_list.append({
                                    'accordion': accordion,
                                    'enabled': cc_enabled,
                                    'name': cc_name,
                                    'face_swapper': cc_face_swapper,
                                    'pixel_boost': cc_pixel_boost,
                                    'use_face_enh': cc_use_face_enh,
                                    'face_enh_model': cc_face_enh_model,
                                    'face_enh_blend': cc_face_enh_blend,
                                    'use_frame_enh': cc_use_frame_enh,
                                    'frame_enh_model': cc_frame_enh_model,
                                    'use_lip_sync': cc_use_lip_sync,
                                    'lip_sync_model': cc_lip_sync_model,
                                    'distance': cc_distance,
                                    'quality': cc_quality,
                                    'exec_provider': cc_exec_provider
                                })

                        custom_launch_btn = gr.Button("🚀 Lancer Tests Personnalisés", variant="primary", size="lg")

                        # Résultats personnalisés
                        with gr.Row():
                            with gr.Column():
                                custom_summary = gr.Textbox(label="Résumé", lines=8)
                            with gr.Column(scale=2):
                                custom_gallery = gr.Gallery(label="📹 Vidéos", columns=3, height=400)
                                custom_player = gr.Video(label="🎬 Lecteur", interactive=False, height=300)
                                custom_path = gr.Textbox(label="📂 Dossier", interactive=False)

        # Footer
        gr.Markdown("""
        ---
        🎬 **Actor Face Swap Studio V3** | Powered by FaceFusion
        """)

        # Event handlers
        def update_config_visibility(num_configs):
            """Affiche/masque les accordions selon le nombre choisi"""
            updates = []
            for i in range(15):
                updates.append(gr.Accordion(visible=(i < num_configs)))
            return updates

        def run_custom_tests_wrapper(source, target, *config_values):
            """Wrapper pour collecter les valeurs des 15 configs et lancer les tests"""
            # config_values contient 14 valeurs par config (15 configs = 210 valeurs)
            # enabled, name, face_swapper, pixel_boost, use_face_enh, face_enh_model, face_enh_blend,
            # use_frame_enh, frame_enh_model, use_lip_sync, lip_sync_model, distance, quality, exec_provider

            configs_data = []
            num_fields = 14
            for i in range(15):
                offset = i * num_fields
                configs_data.append({
                    'enabled': config_values[offset],
                    'name': config_values[offset + 1],
                    'face_swapper': config_values[offset + 2],
                    'pixel_boost': config_values[offset + 3],
                    'use_face_enh': config_values[offset + 4],
                    'face_enh_model': config_values[offset + 5],
                    'face_enh_blend': config_values[offset + 6],
                    'use_frame_enh': config_values[offset + 7],
                    'frame_enh_model': config_values[offset + 8],
                    'use_lip_sync': config_values[offset + 9],
                    'lip_sync_model': config_values[offset + 10],
                    'distance': config_values[offset + 11],
                    'quality': config_values[offset + 12],
                    'exec_provider': config_values[offset + 13]
                })

            return processor.run_custom_batch_tests(source, target, configs_data)

        # Handler pour le bouton de mise à jour
        update_configs_btn.click(
            fn=update_config_visibility,
            inputs=[num_configs_slider],
            outputs=[cfg['accordion'] for cfg in custom_configs_list]
        )

        simple_btn.click(
            fn=processor.process_video_simple,
            inputs=[
                simple_source, simple_target,
                simple_face_swapper, simple_pixel_boost,
                simple_face_enhancer_enable, simple_face_enhancer, simple_face_enhancer_blend,
                simple_frame_enhancer_enable, simple_frame_enhancer,
                simple_lip_sync_enable, simple_lip_sync_model,
                simple_reference_distance, simple_execution_provider, simple_quality
            ],
            outputs=[simple_output_video, simple_output_msg, simple_download_btn]
        )

        batch_predefined_btn.click(
            fn=processor.run_batch_tests,
            inputs=[batch_source, batch_target, batch_predefined_configs],
            outputs=[batch_predefined_summary, batch_predefined_gallery, batch_predefined_path]
        )

        # Collecter tous les inputs des configs personnalisées
        custom_inputs = [batch_source, batch_target]
        for cfg_dict in custom_configs_list:
            custom_inputs.extend([
                cfg_dict['enabled'], cfg_dict['name'], cfg_dict['face_swapper'],
                cfg_dict['pixel_boost'], cfg_dict['use_face_enh'], cfg_dict['face_enh_model'],
                cfg_dict['face_enh_blend'], cfg_dict['use_frame_enh'], cfg_dict['frame_enh_model'],
                cfg_dict['use_lip_sync'], cfg_dict['lip_sync_model'], cfg_dict['distance'],
                cfg_dict['quality'], cfg_dict['exec_provider']
            ])

        custom_launch_btn.click(
            fn=run_custom_tests_wrapper,
            inputs=custom_inputs,
            outputs=[custom_summary, custom_gallery, custom_path]
        )

    return app


def main():
    print("\n🎬 Actor Face Swap Studio V3 - Démarrage...\n")
    print(f"📁 FaceFusion: {FACEFUSION_DIR}")
    print(f"📁 Outputs: {OUTPUTS_DIR}")
    print(f"📁 Batch Results: {BATCH_RESULTS_DIR}\n")

    app = create_gradio_interface()

    print("=" * 60)
    print("✅ Interface prête !")
    print("=" * 60)

    app.launch(
        server_name="0.0.0.0",
        server_port=7862,  # Port différent pour éviter conflit avec V2
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
