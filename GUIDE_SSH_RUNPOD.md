# 🚀 Guide d'utilisation SSH avec RunPod (RTX A6000)

## 🎯 Votre configuration

**Machine distante (RunPod):**
- GPU: RTX A6000 (45 GB VRAM) 🔥
- CPU: Xeon Gold 6226 (48 cores)
- RAM: 48 GB
- IP: `38.29.145.24`
- CUDA: 12.6

**Performances attendues:**
- ⚡ **TRÈS RAPIDE** avec ce GPU
- Preset "Rapide": ~30 secondes par minute de vidéo
- Preset "Équilibré": ~1-2 minutes par minute de vidéo
- Preset "Haute Qualité": ~3-5 minutes par minute de vidéo

---

## 📋 Installation sur le serveur RunPod

### Étape 1: Se connecter au serveur

```bash
ssh root@38.29.145.24
# Ou avec l'utilisateur fourni par RunPod
```

### Étape 2: Cloner votre projet

```bash
# Si vous avez Git configuré
git clone <votre-repo> facefusion-app
cd facefusion-app

# Ou transférez les fichiers depuis votre Mac:
# Sur votre Mac, dans un nouveau terminal:
scp -r "/Users/martinemenguy/Desktop/for facefusion" root@38.29.145.24:~/facefusion-app
```

### Étape 3: Installer sur RunPod

```bash
cd facefusion-app

# Vérifier CUDA
nvidia-smi  # Doit afficher votre RTX A6000

# Installer FaceFusion avec support GPU
cd facefusion
python3 install.py --onnxruntime default
cd ..

# Installer Gradio
pip3 install gradio gradio-rangeslider

# Installer onnxruntime-gpu pour CUDA
pip3 uninstall onnxruntime -y
pip3 install onnxruntime-gpu
```

---

## 🌐 Méthodes d'accès à l'interface

### Méthode 1: Tunnel SSH (RECOMMANDÉE - Sécurisé)

**Sur votre Mac local**, ouvrez un terminal et créez un tunnel:

```bash
ssh -L 7860:localhost:7860 root@38.29.145.24
```

**Sur le serveur RunPod** (dans la session SSH):

```bash
cd facefusion-app
python3 actor_faceswap_studio.py
```

**Sur votre Mac**, ouvrez votre navigateur:
```
http://localhost:7860
```

✅ Avantages:
- Connexion sécurisée (chiffrée)
- Pas besoin d'ouvrir de ports
- Bande passante optimale

### Méthode 2: Accès direct par IP (Nécessite ouverture de port)

**Sur RunPod**, vérifiez que le port 7860 est ouvert dans les paramètres réseau.

**Lancez l'application:**
```bash
cd facefusion-app
python3 actor_faceswap_studio.py
```

**Depuis votre Mac**, ouvrez:
```
http://38.29.145.24:7860
```

⚠️ Attention: Moins sécurisé, utilisez uniquement sur réseau de confiance

### Méthode 3: Gradio Share Link (Temporaire)

Modifiez [actor_faceswap_studio.py](actor_faceswap_studio.py) ligne 535:

```python
share=True,  # Activer le partage public
```

Relancez l'application, Gradio créera un lien public temporaire (72h):
```
https://xxxxx.gradio.live
```

---

## 🚀 Script de lancement optimisé pour SSH

Un script spécial a été créé: **[launch_ssh.sh](launch_ssh.sh)**

**Sur le serveur RunPod:**
```bash
cd facefusion-app
./launch_ssh.sh
```

Ce script:
- ✅ Détecte automatiquement l'IP du serveur
- ✅ N'ouvre pas de navigateur (inutile en SSH)
- ✅ Affiche les instructions de connexion
- ✅ Lance l'application accessible à distance

---

## 💡 Workflow recommandé

### Configuration initiale (une seule fois):

1. **Connectez-vous à RunPod:**
   ```bash
   ssh root@38.29.145.24
   ```

2. **Transférez votre application depuis votre Mac:**
   ```bash
   # Sur votre Mac (nouveau terminal)
   cd "/Users/martinemenguy/Desktop"
   scp -r "for facefusion" root@38.29.145.24:~/facefusion-app
   ```

3. **Installez sur RunPod:**
   ```bash
   # Sur RunPod (via SSH)
   cd ~/facefusion-app
   cd facefusion
   python3 install.py --onnxruntime default
   cd ..
   pip3 install gradio gradio-rangeslider
   pip3 uninstall onnxruntime -y
   pip3 install onnxruntime-gpu
   ```

### Utilisation quotidienne:

1. **Créez le tunnel SSH depuis votre Mac:**
   ```bash
   ssh -L 7860:localhost:7860 root@38.29.145.24
   ```

2. **Dans cette session SSH, lancez l'app:**
   ```bash
   cd ~/facefusion-app
   python3 actor_faceswap_studio.py
   ```

3. **Sur votre Mac, ouvrez votre navigateur:**
   ```
   http://localhost:7860
   ```

4. **Utilisez l'interface normalement !**
   - Upload photo acteur
   - Upload vidéo
   - Choisir preset "Haute Qualité" (vous avez le GPU pour ça !)
   - Traiter

5. **Téléchargez les résultats** directement depuis l'interface

---

## 📊 Optimisations pour RTX A6000

Votre GPU est **très puissant**, utilisez ces paramètres optimaux:

### Paramètres recommandés:

| Paramètre | Valeur | Pourquoi |
|-----------|--------|----------|
| **Preset** | Haute Qualité | Votre GPU peut le gérer facilement |
| **Modèle** | hyperswap_1b_256 | Meilleur qualité |
| **Pixel Boost** | 1024 | Maximum de résolution |
| **Face Enhancer** | Activé | Amélioration maximale |
| **Execution Provider** | cuda | Utiliser le GPU |

### Performances attendues avec ces paramètres:

- Vidéo 1080p, 1 minute: **~3-5 minutes**
- Vidéo 1080p, 5 minutes: **~15-25 minutes**
- Vidéo 4K, 1 minute: **~5-10 minutes**

---

## 🔧 Transfert de fichiers

### Upload de vidéos vers RunPod:

```bash
# Depuis votre Mac
scp "/path/to/your/video.mp4" root@38.29.145.24:~/facefusion-app/uploads/
```

### Téléchargement des résultats depuis RunPod:

**Option 1: Via l'interface Gradio** (recommandé)
- Cliquez sur le menu des 3 points sur la vidéo résultat
- "Download"

**Option 2: Via SCP**
```bash
# Sur votre Mac
scp root@38.29.145.24:~/facefusion-app/outputs/*.mp4 ~/Desktop/
```

---

## 🎯 Exemple complet de session

```bash
# Sur votre Mac - Terminal 1
ssh -L 7860:localhost:7860 root@38.29.145.24

# Une fois connecté (vous êtes sur RunPod)
cd ~/facefusion-app
python3 actor_faceswap_studio.py

# L'application démarre, vous voyez:
# ✅ Interface prête !
# 🌐 Running on local URL:  http://0.0.0.0:7860

# Sur votre Mac - Terminal 2 (ou ouvrez juste le navigateur)
open http://localhost:7860

# L'interface s'ouvre, utilisez-la normalement !
```

---

## 💰 Coûts RunPod

**Votre configuration:**
- $0.024/heure
- RTX A6000

**Estimation des coûts:**
- 1 heure de traitement: **$0.024**
- 10 vidéos de 5 min (preset Haute Qualité): ~4 heures = **$0.096**
- Session de travail de 8h: **$0.192**

💡 **Astuce**: Arrêtez l'instance RunPod quand vous ne l'utilisez pas !

---

## 🆘 Dépannage SSH

### Port 7860 déjà utilisé

```bash
# Sur RunPod, tuer le processus
pkill -f actor_faceswap_studio

# Ou utilisez un autre port
# Modifiez dans actor_faceswap_studio.py: server_port=7861
```

### Tunnel SSH se déconnecte

```bash
# Utilisez autossh pour maintenir le tunnel
autossh -M 0 -L 7860:localhost:7860 root@38.29.145.24

# Ou avec ssh standard + keep-alive
ssh -L 7860:localhost:7860 -o ServerAliveInterval=60 root@38.29.145.24
```

### CUDA non détecté

```bash
# Vérifier CUDA
nvidia-smi

# Réinstaller onnxruntime-gpu
pip3 uninstall onnxruntime onnxruntime-gpu -y
pip3 install onnxruntime-gpu

# Vérifier dans Python
python3 -c "import onnxruntime as ort; print(ort.get_available_providers())"
# Doit afficher: ['CUDAExecutionProvider', 'CPUExecutionProvider']
```

---

## 📱 Accès depuis mobile/tablette

Avec le tunnel SSH actif, vous pouvez aussi accéder depuis mobile:

1. Installez une app de tunnel SSH sur mobile (ex: Termius)
2. Créez le tunnel SSH: `7860:localhost:7860`
3. Ouvrez Safari/Chrome: `http://localhost:7860`

---

## ✅ Checklist de démarrage rapide

- [ ] Connecté à RunPod via SSH
- [ ] Application transférée sur RunPod
- [ ] FaceFusion installé avec GPU (`onnxruntime-gpu`)
- [ ] Tunnel SSH créé depuis Mac (`ssh -L 7860:localhost:7860`)
- [ ] Application lancée sur RunPod
- [ ] Interface accessible sur Mac (`http://localhost:7860`)
- [ ] CUDA détecté (vérifier dans l'interface: provider = cuda)

---

## 🎉 Résumé

**Commande ultime (sur votre Mac):**

```bash
# Terminal 1: Créer le tunnel et se connecter
ssh -L 7860:localhost:7860 root@38.29.145.24 "cd ~/facefusion-app && python3 actor_faceswap_studio.py"

# Ceci fait tout en une commande:
# 1. Crée le tunnel SSH
# 2. Se connecte à RunPod
# 3. Lance l'application
# 4. L'interface est accessible sur http://localhost:7860
```

**Ouvrez votre navigateur:**
```
http://localhost:7860
```

**Et voilà ! Vous avez accès à votre application avec un GPU RTX A6000 !** 🚀

---

**Prêt à traiter des vidéos 100x plus vite qu'en local !** 🎬✨
