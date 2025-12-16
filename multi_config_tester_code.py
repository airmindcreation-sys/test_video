class MultiConfigTester:
    """
    Gestionnaire pour tester plusieurs configurations de face swap
    et comparer les résultats
    """

    def __init__(self, processor: FaceSwapProcessor):
        self.processor = processor
        self.results = []
        self.test_session_dir = None

    def generate_test_combinations(
        self,
        # Paramètres à tester (listes)
        test_face_swapper_models: list,
        test_pixel_boosts: list,
        test_face_enhancer_models: list,
        test_face_enhancer_blends: list,
        test_reference_distances: list,
        test_lip_sync_models: list,
        # Paramètres fixes
        face_enhancer_enabled: bool,
        lip_sync_enabled: bool,
        face_detector_size: str,
        execution_provider: str,
        output_video_quality: int
    ):
        """
        Génère toutes les combinaisons de tests basées sur les paramètres sélectionnés
        """
        import itertools

        # Créer les combinaisons
        combinations = []

        # Si un paramètre n'a qu'une valeur, on le considère comme fixe
        for swapper_model in test_face_swapper_models:
            for pixel_boost in test_pixel_boosts:
                for enhancer_model in test_face_enhancer_models:
                    for enhancer_blend in test_face_enhancer_blends:
                        for ref_distance in test_reference_distances:
                            for lip_model in test_lip_sync_models:
                                config = {
                                    'name': self._generate_config_name(
                                        swapper_model, pixel_boost, enhancer_model,
                                        enhancer_blend, ref_distance, lip_model
                                    ),
                                    'face_swapper_model': swapper_model,
                                    'pixel_boost': pixel_boost,
                                    'face_enhancer': face_enhancer_enabled,
                                    'face_enhancer_model': enhancer_model,
                                    'face_enhancer_blend': enhancer_blend,
                                    'face_detector_size': face_detector_size,
                                    'reference_face_distance': ref_distance,
                                    'lip_sync_enabled': lip_sync_enabled,
                                    'lip_sync_model': lip_model,
                                    'execution_provider': execution_provider,
                                    'output_video_quality': output_video_quality
                                }
                                combinations.append(config)

        return combinations

    def _generate_config_name(self, swapper, pixel, enhancer, blend, distance, lip):
        """Génère un nom court pour la configuration"""
        parts = []
        parts.append(swapper.split('_')[0][:8])  # Premier mot du modèle
        parts.append(f"px{pixel.split('x')[0]}")  # Taille pixel
        parts.append(enhancer[:4])  # 4 premières lettres
        parts.append(f"bl{blend}")  # Blend
        parts.append(f"d{distance}".replace('.', ''))  # Distance
        parts.append(lip.split('_')[0][:6])  # Type lip sync
        return "_".join(parts)

    def run_multi_tests(
        self,
        source_image_path: str,
        target_video_path: str,
        test_configs: list,
        progress=gr.Progress()
    ):
        """
        Exécute tous les tests de configuration séquentiellement
        """
        import time
        from datetime import datetime

        # Validation des fichiers
        valid, message = self.processor.validate_inputs(source_image_path, target_video_path)
        if not valid:
            return [], message

        # Créer un dossier pour cette session de tests
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_session_dir = OUTPUTS_DIR / f"multi_test_{timestamp}"
        self.test_session_dir.mkdir(exist_ok=True)

        self.results = []
        total_configs = len(test_configs)

        for i, config in enumerate(test_configs):
            progress((i / total_configs), desc=f"Test {i+1}/{total_configs}: {config['name']}")

            # Créer le nom du fichier de sortie
            output_filename = f"{config['name']}.mp4"
            output_path = str(self.test_session_dir / output_filename)

            # Construire la commande
            cmd = self.processor.build_command(
                source_image_path,
                target_video_path,
                output_path,
                config['face_swapper_model'],
                config['pixel_boost'],
                config['face_enhancer'],
                config['face_enhancer_model'],
                str(config['face_enhancer_blend']),
                config['face_detector_size'],
                str(config['reference_face_distance']),
                config['lip_sync_enabled'],
                config['lip_sync_model'],
                config['execution_provider'],
                config['output_video_quality']
            )

            print(f"\n{'='*60}")
            print(f"Test {i+1}/{total_configs}: {config['name']}")
            print(f"{'='*60}")
            print(f"Commande: {' '.join(cmd)}\n")

            start_time = time.time()

            try:
                # Lancer la commande
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    cwd=str(FACEFUSION_DIR)
                )

                # Lire la sortie
                for line in process.stdout:
                    print(line.rstrip())

                # Attendre la fin
                return_code = process.wait()
                execution_time = time.time() - start_time

                if return_code == 0 and os.path.exists(output_path):
                    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                    result = {
                        'config': config,
                        'output_path': output_path,
                        'output_filename': output_filename,
                        'execution_time': round(execution_time, 2),
                        'file_size_mb': round(file_size, 2),
                        'status': 'success'
                    }
                    print(f"✓ Succès! Temps: {execution_time:.2f}s, Taille: {file_size:.2f} MB")
                else:
                    result = {
                        'config': config,
                        'status': 'failed',
                        'error': f"Return code: {return_code}"
                    }
                    print(f"✗ Échec: code {return_code}")

            except Exception as e:
                result = {
                    'config': config,
                    'status': 'failed',
                    'error': str(e)
                }
                print(f"✗ Erreur: {e}")

            self.results.append(result)

        progress(1.0, desc="✅ Tous les tests terminés!")

        # Retourner les résultats pour affichage
        return self.results, self._generate_summary()

    def _generate_summary(self):
        """Génère un résumé textuel des résultats"""
        successful = [r for r in self.results if r['status'] == 'success']
        failed = [r for r in self.results if r['status'] == 'failed']

        summary = f"""
✅ Tests terminés: {len(self.results)}
✓ Réussis: {len(successful)}
✗ Échoués: {len(failed)}

📁 Dossier de sortie: {self.test_session_dir}

{'='*60}
RÉSULTATS DÉTAILLÉS
{'='*60}

"""

        for i, result in enumerate(self.results, 1):
            if result['status'] == 'success':
                summary += f"""
{i}. ✓ {result['config']['name']}
   Temps: {result['execution_time']}s
   Taille: {result['file_size_mb']} MB
   Fichier: {result['output_filename']}
"""
            else:
                summary += f"""
{i}. ✗ {result['config']['name']}
   Erreur: {result.get('error', 'Unknown')}
"""

        return summary

    def get_result_videos(self):
        """
        Retourne la liste des vidéos générées pour la galerie
        """
        videos = []
        for result in self.results:
            if result['status'] == 'success':
                videos.append({
                    'path': result['output_path'],
                    'label': result['config']['name'],
                    'metadata': result
                })
        return videos


# Instance globale du multi-tester
multi_tester = None
