# ⚡ Configuration rapide pour serveur RunPod

## 🚀 Installation express (copier-coller)

Une fois connecté en SSH à votre serveur RunPod:

```bash
# 1. Vérifier CUDA
nvidia-smi

# 2. Installer Python et dépendances système
apt-get update
apt-get install -y python3-pip ffmpeg curl git

# 3. Aller dans votre dossier
cd ~/facefusion-app

# 4. Installer FaceFusion
cd facefusion
python3 install.py --onnxruntime default
cd ..

# 5. Installer Gradio
pip3 install gradio gradio-rangeslider

# 6. IMPORTANT: Installer onnxruntime-gpu pour CUDA
pip3 uninstall onnxruntime -y
pip3 install onnxruntime-gpu

# 7. Vérifier que CUDA est détecté
python3 -c "import onnxruntime as ort; print('GPU OK!' if 'CUDAExecutionProvider' in ort.get_available_providers() else 'GPU NON DÉTECTÉ')"

# 8. Lancer l'application
python3 actor_faceswap_studio.py
```

---

## 🌐 Accès depuis votre Mac

**Terminal sur votre Mac:**
```bash
ssh -L 7860:localhost:7860 root@38.29.145.24
```

**Navigateur sur votre Mac:**
```
http://localhost:7860
```

---

## 📦 Transférer votre application vers RunPod

**Sur votre Mac:**
```bash
cd "/Users/martinemenguy/Desktop"
tar -czf facefusion-app.tar.gz "for facefusion"
scp facefusion-app.tar.gz root@38.29.145.24:~/
```

**Sur RunPod (via SSH):**
```bash
cd ~
tar -xzf facefusion-app.tar.gz
mv "for facefusion" facefusion-app
cd facefusion-app
```

---

## 🎯 Script d'installation automatique

Créez un fichier `setup_runpod.sh` sur RunPod:

```bash
cat > ~/setup_runpod.sh << 'EOF'
#!/bin/bash

echo "🚀 Installation Actor Face Swap Studio sur RunPod"

# Mise à jour système
apt-get update -y
apt-get install -y python3-pip ffmpeg curl git

# Installation de l'application
cd ~/facefusion-app || exit 1

# FaceFusion
cd facefusion
python3 install.py --onnxruntime default
cd ..

# Gradio
pip3 install gradio gradio-rangeslider

# GPU support
pip3 uninstall onnxruntime -y
pip3 install onnxruntime-gpu

# Vérification
echo ""
echo "✅ Vérification de CUDA..."
python3 -c "
import onnxruntime as ort
providers = ort.get_available_providers()
if 'CUDAExecutionProvider' in providers:
    print('✅ GPU CUDA détecté et prêt !')
else:
    print('❌ GPU NON DÉTECTÉ - vérifiez onnxruntime-gpu')
    exit(1)
"

echo ""
echo "🎉 Installation terminée !"
echo ""
echo "Pour lancer l'application:"
echo "  cd ~/facefusion-app"
echo "  python3 actor_faceswap_studio.py"
EOF

chmod +x ~/setup_runpod.sh
bash ~/setup_runpod.sh
```

---

## 💡 Variables d'environnement optimales pour RTX A6000

```bash
# Optimisations CUDA pour RTX A6000
export CUDA_VISIBLE_DEVICES=0
export OMP_NUM_THREADS=8
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

Ajoutez au début de `actor_faceswap_studio.py` ou dans votre `.bashrc`:

```bash
echo "export OMP_NUM_THREADS=8" >> ~/.bashrc
echo "export CUDA_VISIBLE_DEVICES=0" >> ~/.bashrc
source ~/.bashrc
```

---

## 📊 Monitoring GPU en temps réel

**Pendant le traitement, surveillez votre GPU:**

```bash
# Terminal séparé sur RunPod
watch -n 1 nvidia-smi
```

Vous verrez:
- Utilisation GPU (devrait être ~80-100% pendant le traitement)
- VRAM utilisée (~5-15 GB selon le preset)
- Température

---

## 🔥 Performances attendues RTX A6000

| Vidéo | Preset | Temps de traitement |
|-------|--------|---------------------|
| 1080p, 1 min | Rapide | ~30 sec |
| 1080p, 1 min | Équilibré | ~1-2 min |
| 1080p, 1 min | Haute Qualité | ~3-5 min |
| 1080p, 10 min | Haute Qualité | ~30-50 min |
| 4K, 1 min | Haute Qualité | ~5-10 min |

**Avec CPU uniquement (pour comparaison):**
- Même vidéo = **10-20x plus lent**

---

## 🛡️ Sécurité

### Option 1: Tunnel SSH uniquement (RECOMMANDÉ)
- Pas besoin d'ouvrir de ports
- Connexion chiffrée
- Accès uniquement depuis votre Mac

### Option 2: Authentification par mot de passe
Modifiez `actor_faceswap_studio.py` pour ajouter une authentification:

```python
app.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    auth=("admin", "votre_mot_de_passe_fort"),  # Ajouter cette ligne
    show_error=True
)
```

---

## 🔄 Automatisation avec tmux

Pour garder l'application en arrière-plan après déconnexion SSH:

```bash
# Installer tmux
apt-get install -y tmux

# Créer une session
tmux new -s facefusion

# Lancer l'application
cd ~/facefusion-app
python3 actor_faceswap_studio.py

# Détacher: Ctrl+B puis D
# L'application continue de tourner

# Se reconnecter plus tard
tmux attach -t facefusion
```

---

## 🎯 Commande ultime tout-en-un

**Sur votre Mac (une seule commande):**

```bash
ssh -L 7860:localhost:7860 root@38.29.145.24 \
  "cd ~/facefusion-app && \
   export CUDA_VISIBLE_DEVICES=0 && \
   python3 actor_faceswap_studio.py"
```

Puis ouvrez: http://localhost:7860

---

**Vous êtes prêt à exploiter toute la puissance de votre RTX A6000 !** 🚀
