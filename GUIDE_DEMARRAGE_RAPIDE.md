# 🚀 Guide de Démarrage Rapide - Actor Face Swap Studio

**Temps estimé: 10-15 minutes**

Ce guide vous permettra de lancer votre application de face swap en quelques étapes simples.

---

## ✅ Checklist avant de commencer

- [ ] Python 3.10+ installé
- [ ] ffmpeg installé
- [ ] 5 GB d'espace disque disponible
- [ ] Connexion internet (pour télécharger les modèles)
- [ ] (Optionnel) GPU NVIDIA avec CUDA pour de meilleures performances

---

## 📦 Installation en 3 étapes

### Étape 1: Installer FaceFusion (2-3 minutes)

```bash
# Naviguer dans le dossier facefusion
cd facefusion

# Lancer l'installation
python install.py

# Revenir au dossier parent
cd ..
```

Cette commande va télécharger et installer tous les composants nécessaires de FaceFusion.

### Étape 2: Installer les dépendances de l'application (1-2 minutes)

```bash
pip install -r requirements_app.txt
```

### Étape 3: Lancer l'application

**Option A - Avec le script de lancement (recommandé):**

**macOS/Linux:**
```bash
./launch.sh
```

**Windows:**
```batch
launch.bat
```

**Option B - Lancement manuel:**
```bash
python actor_faceswap_studio.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse: `http://localhost:7860`

---

## 🎬 Premier test (5 minutes)

### 1. Préparez vos fichiers
- **Photo source**: Une photo claire du visage de votre acteur
- **Vidéo test**: Utilisez d'abord une courte vidéo (5-10 secondes) pour tester

### 2. Dans l'interface web

1. **Uploadez** votre photo dans "Portrait de l'acteur"
2. **Uploadez** votre vidéo dans "Vidéo cible"
3. **Sélectionnez** le preset "⚡ Rapide" (pour le premier test)
4. **Cliquez** sur "🚀 Lancer le Face Swap"
5. **Attendez** (environ 30 secondes à 2 minutes pour une vidéo de 10 secondes)
6. **Visionnez** et téléchargez le résultat !

---

## 🎯 Workflow recommandé pour la production

Une fois votre premier test réussi:

### Pour des résultats professionnels:

1. **Testez d'abord avec "Rapide"** sur un court extrait (5-10 sec)
2. Si le résultat est satisfaisant, **passez au preset "Équilibré"**
3. Pour la vidéo complète, utilisez **"Équilibré"** ou **"Haute Qualité"**

### Ajustements si nécessaire:

Dans "Paramètres avancés", vous pouvez modifier:
- **Intensité du swap** (0.5 à 1.0) - Réduire si le résultat n'est pas naturel
- **Face Enhancer** - Toujours activé pour de meilleurs résultats
- **Pixel Boost** - 512 est un bon compromis
- **Flou du masque** - Augmenter si les bords sont trop nets

---

## ⚡ Optimisation des performances

### Si vous avez un GPU NVIDIA:

1. Installez le support CUDA:
```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

2. Dans l'interface, vérifiez que "Provider d'exécution" = **cuda**

**Gain de performance: 5-10x plus rapide qu'en CPU !**

### Si vous utilisez le CPU uniquement:

- Utilisez le preset **"Rapide"**
- Réduisez la résolution vidéo avant traitement si possible
- Testez sur de courts extraits
- Patience recommandée pour les vidéos longues

---

## 📊 Temps de traitement estimés

**Avec GPU NVIDIA (CUDA):**
- Rapide: ~1-2 min par minute de vidéo
- Équilibré: ~3-5 min par minute
- Haute Qualité: ~10-15 min par minute

**Avec CPU uniquement:**
- Rapide: ~5-10 min par minute de vidéo
- Équilibré: ~15-25 min par minute
- Haute Qualité: ~30-60 min par minute (non recommandé)

**Exemple:**
- Vidéo de 3 minutes avec preset "Équilibré" + GPU = **~10-15 minutes**
- Vidéo de 3 minutes avec preset "Équilibré" + CPU = **~45-75 minutes**

---

## 🆘 Problèmes courants

### "No faces detected"
➡️ Assurez-vous que le visage est bien visible et net dans la photo source

### Traitement très lent
➡️ Vérifiez que vous utilisez le preset "Rapide" ou que CUDA est activé si vous avez un GPU

### Erreur de mémoire
➡️ Réduisez le Pixel Boost à 256 ou utilisez le preset "Rapide"

### L'application ne se lance pas
➡️ Vérifiez que toutes les dépendances sont installées:
```bash
pip install -r requirements_app.txt --force-reinstall
```

---

## 💡 Conseils pro

1. **Éclairage cohérent**: Choisissez une photo source avec un éclairage similaire à la vidéo
2. **Angle de vue**: Les meilleurs résultats sont obtenus quand l'angle du visage est similaire
3. **Tests itératifs**: Testez plusieurs photos sources si le résultat n'est pas satisfaisant
4. **Sauvegardez vos résultats**: Les fichiers sont dans le dossier `outputs/`

---

## 📁 Où trouver mes fichiers ?

```
for facefusion/
├── outputs/                    ← Vos vidéos traitées sont ici !
│   └── faceswap_mavideo_equilibre.mp4
├── uploads/                    ← Photos uploadées (temporaire)
└── temp/                       ← Fichiers temporaires (nettoyés auto)
```

---

## 🎓 Aller plus loin

Une fois à l'aise avec l'interface:

- **Explorez les paramètres avancés** pour un contrôle fin
- **Testez différents modèles** de face swap
- **Ajustez les masques** pour des cas spécifiques
- **Lisez le README complet** ([README_APP.md](README_APP.md)) pour tous les détails

---

## 🎉 Vous êtes prêt !

Lancez l'application et commencez à créer vos face swaps professionnels !

```bash
# macOS/Linux
./launch.sh

# Windows
launch.bat
```

---

**Des questions ?** Consultez le [README_APP.md](README_APP.md) pour la documentation complète.

**Bon face swapping ! 🎬✨**
